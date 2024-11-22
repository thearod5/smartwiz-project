import os
from typing import Dict, List, Optional, Type, TypeVar

from anthropic import Anthropic
from anthropic.types import ToolUseBlock
from dotenv import load_dotenv
from pydantic import BaseModel

from rate_limited_batcher.thread_util import ThreadUtil

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

GenericResponseType = TypeVar("GenericResponseType", bound=BaseModel)


def complete_batch(prompts: List[str], tool: Type[GenericResponseType]) -> List[GenericResponseType]:
    """
    Completes batch of prompts and parses response into tool calls.
    :param prompts: The prompts to complete and parse.
    :param tool: The base model of the tool to parse response into.
    :return: List of parsed tools
    """
    state = ThreadUtil.multi_thread_process(
        "Completing batch prompts",
        prompts,
        thread_work=lambda p: complete_tool(p, tool),
        n_threads=10,
        collect_results=True
    )
    completions = state.results
    return completions


def complete_tools(messages: List[Dict],
                   system: str,
                   tools: List[Type[GenericResponseType]],
                   max_prompt_length: int = 300_000,
                   retries: int = 2) -> Optional[GenericResponseType]:
    """
    Prompts LLM to make single tool call on prompt.
    :param messages: The messages in the chat.
    :param system: The system prompt.
    :param tools: The tool to parse response into.
    :param max_prompt_length: The max length of prompt in characters.
    :param retries: The number of times to retry prompt.
    :return: Parsed Response
    """
    tool_schemas = [create_tool_call(tool) for tool in tools]
    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",  # TODO: Make constant and better way to interchange models,
        max_tokens=5_000,
        tools=tool_schemas,
        messages=messages,
        system=system,
        tool_choice={"type": "any"},
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    )
    tool_use_block_query = [b for b in response.content if b.type == "tool_use"]
    if len(tool_use_block_query) == 0:
        raise Exception("Model did not select tool for messages: {}".format(messages))
    tool_use_block: ToolUseBlock = tool_use_block_query[0]
    tool_query = [tool for tool in tools if tool.schema()["title"] == tool_use_block.name]
    assert len(tool_query) == 1, f"Selected ({len(tool_query)}) tools."
    selected_tool = tool_query[0]
    tool_instance = selected_tool(**tool_use_block.input)
    return tool_instance


def complete_tool(prompt: str,
                  tool: Type[GenericResponseType],
                  max_prompt_length: int = 300_000,
                  retries: int = 2) -> Optional[GenericResponseType]:
    """
    Prompts LLM to make single tool call on prompt.
    :param prompt: The prompt to complete.
    :param tool: The tool to parse response into.
    :param max_prompt_length: The max length of prompt in characters.
    :param retries: The number of times to retry prompt.
    :return: Parsed Response
    """
    prompt = prompt[:max_prompt_length]
    tool_schema = create_tool_call(tool)
    response = anthropic.messages.create(
        model="claude-3-5-haiku-20241022",  # "claude-3-5-sonnet-20241022",
        max_tokens=5_000,
        tools=[tool_schema],
        messages=[{"role": "user", "content": prompt}],
        tool_choice={"type": "tool", "name": tool_schema["name"]},
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    )
    tool_use_block: ToolUseBlock = response.content[0]
    try:

        tool_instance = tool(**tool_use_block.input)
    except Exception as e:
        if retries == 0:
            return None

        new_prompt = prompt + ("\n\nYour last response failed to follow the format. "
                               "Please pay more attention to following the expected response format. ")
        return complete_tool(new_prompt, tool, max_prompt_length=max_prompt_length, retries=retries - 1)
    return tool_instance


def create_tool_call(tool_class: Type[GenericResponseType]) -> Dict:
    tool_schema = tool_class.schema()
    tool_name = tool_schema["title"]

    if "$defs" in tool_schema:
        tool_defs = tool_schema["$defs"]
        properties = {
            k: get_sub_schema(k_schema, tool_defs) for k, k_schema in tool_schema["properties"].items()
        }
    else:
        properties = tool_schema["properties"]

    tool_json = {
        "name": tool_name,
        "description": tool_schema["description"],
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": tool_schema["required"],
        },
    }
    return tool_json


def get_sub_schema(schema, tool_defs):
    if "items" in schema:
        item_entity = os.path.basename(schema["items"]["$ref"])
        schema["items"] = tool_defs[item_entity]
    return schema

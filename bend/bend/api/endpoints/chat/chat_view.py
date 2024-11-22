import os.path
from typing import Dict, List, Tuple

from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.chat.chat_serializer import ChatHistorySerializer
from api.endpoints.chat.models import AskFollowup, SelectItems
from api.endpoints.chat.prompts import CHAT_PROMPT
from api.models import Address, User
from api.utils.fs import read_json
from api.utils.llm import complete_tools


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """

        :param request:
        :return:
        """
        # Deserialize the incoming request
        serializer = ChatHistorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract messages from the chat history
        chat_history = serializer.validated_data.get("messages", [])
        tool_call = chat_agent(request.user, chat_history)

        if isinstance(tool_call, SelectItems):
            form_data = get_form_data(tool_call)
            response = {"response": None, "form": form_data}
        elif isinstance(tool_call, AskFollowup):
            response = {"response": tool_call.response, "form": None}
        else:
            raise Exception(f"Unknown tool call: {tool_call}")
        return JsonResponse(response)


def chat_agent(user: User, chat_history: List[Dict]):
    if user.primary_address is None:
        raise Exception("User must have primary address.")

    credits, deductions = query_tax_items(user.primary_address)

    system_prompt = CHAT_PROMPT.format(format_items(credits), format_items(deductions))

    if len(chat_history) == 0:
        chat_history.append({"role": "user", "content": "Hi, Claude."})

    tool_call = complete_tools(chat_history, system=system_prompt, tools=[AskFollowup, SelectItems])
    return tool_call


def get_form_data(tool: SelectItems):
    items = retrieve_mock_items()
    name2item = {i["name"]: i for i in items}

    items = []
    for credit in (tool.credits + tool.deductions):
        credit_name = credit.name
        if credit_name not in name2item:
            continue
        item = name2item[credit_name]
        items.append({
            "type": item["type"],
            "name": credit.name,
            "explanation": credit.explanation,
            "description": item["description"],
            "amount": try_parse_int(credit.amount, 0),
            "source": item["source"]
        })
    return {
        "items": items,
        "salary": tool.salary
    }


def try_parse_int(value: str, default) -> int:
    try:
        return int(value)
    except:
        return default


def query_tax_items(address: Address) -> Tuple[List[Dict], List[Dict]]:
    tax_items = retrieve_mock_items()
    credits = [i for i in tax_items if i["type"] == "credit"]
    deductions = [i for i in tax_items if i["type"] == "deduction"]
    return credits, deductions


def retrieve_mock_items():
    # TODO: Look up questions based on address
    file_location = os.environ["ITEM_FILE_PATH"]
    tax_items = read_json(file_location)[0]
    return tax_items


def format_items(items: List[Dict]):
    lines = []
    for item in items:
        if "name" in item and "description" in item:
            lines.append(f"Name: {item['name']}\n{item['description']}")
    return "\n\n".join(lines)


def format_chat(messages: List[Dict]):
    lines = []
    for message in messages:
        lines.append(f"Role: {message['role']}\n{message['content']}")
    prompt = "\n\n".join(lines)
    if len(messages) == 0:
        prompt = "There are no messages in chat yet. Send your first question to start the converstation."
    return prompt

import React from "react";
import {Accordion, AccordionDetails, AccordionSummary, IconButton, Link, Typography,} from "@mui/material";
import {Delete, Edit, ExpandMore} from "@mui/icons-material";
import {TaxItem} from "../states/formState";

interface TaxItemListProps {
    title: string;
    items: TaxItem[];
    onEdit: (item: TaxItem) => void;
    onDelete: (id: string) => void;
}

const TaxItemList: React.FC<TaxItemListProps> = ({title, items, onEdit, onDelete}) => (
    <div style={{flex: 1}}>
        <Typography variant="h6" gutterBottom>
            {title}
        </Typography>
        {items.map((item) => (
            <Accordion key={item.name}>
                <AccordionSummary expandIcon={<ExpandMore/>}>
                    <Typography>
                        {item.name} - ${item.amount.toFixed(2)}
                    </Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <div style={{display: "flex", flexDirection: "column"}}>
                        <Typography variant="body1" gutterBottom>
                            {item.description}
                        </Typography>
                        <Typography variant="body2" gutterBottom>
                            <strong>Explanation:</strong> {item.explanation}
                        </Typography>
                        <Typography variant="body2" gutterBottom>
                            <strong>Source:</strong>{" "}
                            <Link href={item.source} target="_blank" rel="noopener">
                                {item.source}
                            </Link>
                        </Typography>
                        <div style={{marginTop: "14px"}}>
                            <IconButton onClick={() => onEdit(item)}>
                                <Edit/>
                            </IconButton>
                            <IconButton onClick={() => onDelete(item.id)}>
                                <Delete/>
                            </IconButton>
                        </div>
                    </div>
                </AccordionDetails>
            </Accordion>
        ))}
    </div>
);

export default TaxItemList;

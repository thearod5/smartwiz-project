import React, {useState} from "react";
import {Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField} from "@mui/material";
import {TaxItem} from "../states/formState";

interface TaxItemFormProps {
    open: boolean;
    onClose: () => void;
    onSave: (item: TaxItem) => void;
    initialData: TaxItem;
}

const TaxItemForm: React.FC<TaxItemFormProps> = ({open, onClose, onSave, initialData}) => {
    const [form, setForm] = useState<TaxItem>(initialData);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setForm((prev) => ({
            ...prev,
            [name]: name === "amount" ? parseFloat(value) || 0 : value,
        }));
    };

    const handleSave = () => {
        onSave(form);
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{initialData ? "Edit Tax Item" : "Add Tax Item"}</DialogTitle>
            <DialogContent>
                <TextField
                    fullWidth
                    margin="dense"
                    label="Type"
                    name="type"
                    value={form.type}
                    onChange={handleChange}
                    select
                    SelectProps={{native: true}}
                >
                    <option value="credit">Credit</option>
                    <option value="deduction">Deduction</option>
                </TextField>
                <TextField
                    fullWidth
                    margin="dense"
                    label="Name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="dense"
                    label="Amount"
                    name="amount"
                    type="number"
                    value={form.amount}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="dense"
                    label="Description"
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="dense"
                    label="Explanation"
                    name="explanation"
                    value={form.explanation}
                    onChange={handleChange}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={handleSave} variant="contained">
                    Save
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default TaxItemForm;

import React, {useState} from "react";
import {Box, Button, TextField, Typography,} from "@mui/material";
import {Add} from "@mui/icons-material";
import useFormState, {TaxItem} from "../states/formState";
import TaxItemList from "../components/TaxItemList";
import TaxItemForm from "../components/TaxItemForm";
import {useNavigate} from "react-router-dom";


const TaxReturnForm: React.FC = () => {
    const {salary, credits, deductions, addTaxItem, updateTaxItem} = useFormState();
    const [editingItem, setEditingItem] = useState<TaxItem | null>(null);
    const [showForm, setShowForm] = useState(false);
    const navigate = useNavigate();

    const handleAddOrEdit = (item: TaxItem) => {
        if (editingItem) {
            updateTaxItem(editingItem.id, item);
        } else {
            addTaxItem({...item, id: Date.now().toString()});
        }
        setShowForm(false);
        setEditingItem(null);
    };

    const handleEdit = (item: TaxItem) => {
        setEditingItem(item);
        setShowForm(true);
    };

    const handleDelete = (id: string) => {
        updateTaxItem(id, {amount: 0, name: "[Deleted]", description: "", explanation: ""});
    };

    const handleSubmit = () => {
        navigate("/summary")
    };


    const totalCredits = credits.reduce((sum, item) => sum + item.amount, 0);
    const totalDeductions = deductions.reduce((sum, item) => sum + item.amount, 0);

    const totalTaxableIncome = salary - totalDeductions + totalCredits;

    return (
        <Box sx={{padding: 2, maxWidth: 800, margin: "0 auto"}}>
            <Typography variant="h4" gutterBottom>
                Tax Return Form
            </Typography>
            <Box sx={{marginBottom: 2}}>
                <TextField
                    label="Salary"
                    variant="outlined"
                    fullWidth
                    value={salary}
                    onChange={(e) => useFormState.setState({salary: parseFloat(e.target.value) || 0})}
                    type="number"
                />
            </Box>
            <Box sx={{display: "flex", gap: 4}}>
                <TaxItemList
                    title="Credits"
                    items={credits}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
                <TaxItemList
                    title="Deductions"
                    items={deductions}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
            </Box>
            <Button
                startIcon={<Add/>}
                variant="contained"
                color="primary"
                sx={{marginTop: 2}}
                onClick={() => setShowForm(true)}
            >
                Add Tax Item
            </Button>
            <Typography variant="h6" sx={{marginTop: 2}}>
                Total Credits: ${totalCredits.toFixed(2)}
            </Typography>
            <Typography variant="h6">
                Total Deductions: ${totalDeductions.toFixed(2)}
            </Typography>
            <Typography variant="h6">
                Taxable Income: ${totalTaxableIncome.toFixed(2)}
            </Typography>
            <Button
                variant="contained"
                color="secondary"
                sx={{marginTop: 2}}
                size={"large"}
                onClick={handleSubmit}
            >
                Submit
            </Button>
            {
                editingItem === null ? null : <TaxItemForm
                    open={showForm}
                    onClose={() => setShowForm(false)}
                    onSave={handleAddOrEdit}
                    initialData={editingItem}
                />
            }

        </Box>
    );
};

export default TaxReturnForm;

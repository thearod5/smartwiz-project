import React, {useEffect, useState} from 'react';
import {Box, Button, Divider, List, ListItem, ListItemText, Paper, Typography} from '@mui/material';
import useFormState from "../states/formState";
import apiClient from "../api/api";
import useReceiptState from "../states/receiptState";
import {useAppState} from "../states/appState";
import {useNavigate} from "react-router-dom";

type TaxBracket = {
    rate: number;
    min: number;
    max: number | null;
};

const taxBrackets: TaxBracket[] = [
    {rate: 0.10, min: 0, max: 11000},
    {rate: 0.12, min: 11001, max: 44725},
    {rate: 0.22, min: 44726, max: 95375},
    {rate: 0.24, min: 95376, max: 182100},
    {rate: 0.32, min: 182101, max: 231250},
    {rate: 0.35, min: 231251, max: 578125},
    {rate: 0.37, min: 578126, max: null}
];

function calculateTaxableIncome(annualIncome: number, deductions: number): number {
    return annualIncome - deductions;
}

function calculateTaxesOwed(taxableIncome: number): number {
    let taxesOwed = 0;

    for (const bracket of taxBrackets) {
        if (taxableIncome > bracket.min) {
            const upperLimit = bracket.max ?? taxableIncome;
            const incomeInBracket = Math.min(taxableIncome, upperLimit) - bracket.min;
            taxesOwed += incomeInBracket * bracket.rate;

            if (bracket.max && taxableIncome <= bracket.max) break;
        }
    }

    return taxesOwed;
}

function calculateRefund(credits: number, taxesOwed: number): number {
    return credits - taxesOwed;
}

const ITEM_NAMES = ["Illinois School Credit", "Illinois Home Ownership", "Illinois Standard Deduction for Non-Home Owners"];

const TaxReturnPage: React.FC = () => {
    const [summary, setSummary] = useState<{
        taxableIncome: number;
        taxesOwed: number;
        refund: number;
        totalDeduction: number;
        totalCredits: number;
    } | null>(null);
    const {salary, credits, deductions} = useFormState();
    const {setReceiptData} = useReceiptState.getState();
    const {setLoading} = useAppState.getState();
    const navigate = useNavigate();

    useEffect(() => {
        const totalDeductionAmount = deductions
            .filter(d => ITEM_NAMES.includes(d.name))
            .reduce((acc, d) => acc + d.amount, 0);
        const totalCreditAmount = credits
            .filter(d => ITEM_NAMES.includes(d.name))
            .reduce((acc, d) => acc + d.amount, 0);

        const taxableIncome = calculateTaxableIncome(salary, totalDeductionAmount);
        const taxesOwed = calculateTaxesOwed(taxableIncome);
        const refund = calculateRefund(totalCreditAmount, taxesOwed);

        setSummary({
            taxableIncome,
            taxesOwed,
            refund,
            totalDeduction: totalDeductionAmount,
            totalCredits: totalCreditAmount
        });
    }, [salary, credits, deductions]);

    const handleSubmit = async () => {
        if (!summary) {
            alert("Calculation has not finished...");
            return
        }
        const attended_school = credits.filter(c => c.name === "Illinois School Credit").length > 0
        const owned_home = deductions.filter(c => c.name === "Illinois Home Ownership").length > 0

        const payload = {
            year: (new Date().getFullYear()),
            annualIncome: salary,
            attended_school,
            owned_home
        }

        setLoading(true)
        apiClient.post("/return", payload).then((returnCreationResponse) => {
            const taxReturn = returnCreationResponse.data
            console.log("Return:", taxReturn)
            apiClient.post("/submit", {"returnId": taxReturn.id}).then((submitResponse) => {
                setReceiptData(submitResponse.data)
                navigate("/receipt")
            }).finally(() => setLoading(false))
        })

    };
    const getAmountStyle = (refund: number) => ({
        color: refund >= 0 ? 'green' : 'red',
        fontWeight: 'bold'
    });

    return (
        <Box sx={{p: 4, maxWidth: 700, mx: 'auto'}}>
            {summary && (
                <Paper sx={{p: 3, mb: 3}}>
                    <Typography variant="h4" gutterBottom>
                        Tax Return Summary
                    </Typography>
                    <Divider sx={{mb: 2}}/>
                    <Typography variant="h6">Step 1: Deductions</Typography>
                    <List>
                        {deductions.filter(d => ITEM_NAMES.includes(d.name)).map((d, index) => (
                            <ListItem key={index}>
                                <ListItemText primary={`${d.name}: $${d.amount.toFixed(2)}`}/>
                            </ListItem>
                        ))}
                        <ListItem>
                            <ListItemText primary={`Total Deductions: $${summary.totalDeduction.toFixed(2)}`}/>
                        </ListItem>
                    </List>
                    <Divider sx={{my: 2}}/>
                    <Typography variant="h6">Step 2: Taxable Income</Typography>
                    <Typography>
                        Annual Salary: ${salary.toFixed(2)} - Deductions: ${summary.totalDeduction.toFixed(2)} =
                        Taxable Income: ${summary.taxableIncome.toFixed(2)}
                    </Typography>
                    <Divider sx={{my: 2}}/>
                    <Typography variant="h6">Step 3: Taxes Owed</Typography>
                    <Typography>
                        Based on the federal tax brackets, the taxes owed are calculated to be:
                        ${summary.taxesOwed.toFixed(2)}
                    </Typography>
                    <Divider sx={{my: 2}}/>
                    <Typography variant="h6">Step 4: Credits and Refund</Typography>
                    <List>
                        {credits.filter(c => ITEM_NAMES.includes(c.name)).map((c, index) => (
                            <ListItem key={index}>
                                <ListItemText primary={`${c.name}: $${c.amount.toFixed(2)}`}/>
                            </ListItem>
                        ))}
                        <ListItem>
                            <ListItemText primary={`Total Credits: $${summary.totalCredits.toFixed(2)}`}/>
                        </ListItem>
                    </List>
                    <Typography>
                        {summary.refund >= 0 ? (
                            <>
                                Refund = Total Credits (${summary.totalCredits.toFixed(2)}) - Taxes Owed
                                (${summary.taxesOwed.toFixed(2)}) =
                                <span style={getAmountStyle(summary.refund)}>
                                    ${summary.refund.toFixed(2)}
                                </span>
                            </>
                        ) : (
                            <>
                                Taxes Owed = Taxes Owed (${summary.taxesOwed.toFixed(2)}) - Total Credits
                                (${summary.totalCredits.toFixed(2)}) =
                                <span style={getAmountStyle(summary.refund)}>
                                    ${Math.abs(summary.refund).toFixed(2)}
                                </span>
                            </>
                        )}
                    </Typography>
                </Paper>
            )}

            <Button
                variant="contained"
                color="secondary"
                fullWidth
                onClick={handleSubmit}
                disabled={!summary}
            >
                Generate Tax Return
            </Button>
        </Box>
    );
};

export default TaxReturnPage;

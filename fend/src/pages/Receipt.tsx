import React from 'react';
import {Box, Grid, Paper, Typography} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import useReceiptStore from "../states/receiptState";


const Receipt: React.FC = () => {
    const data = useReceiptStore((state) => state.data);

    if (!data) {
        return (
            <Typography variant="h6" textAlign="center">
                No receipt data available.
            </Typography>
        );
    }
    return (
        <Paper elevation={3} sx={{padding: 4, maxWidth: 600, margin: 'auto'}}>
            <Box textAlign="center" mb={4}>
                <CheckCircleOutlineIcon color="success" sx={{fontSize: 80}}/>
                <Typography variant="h5" component="h1" fontWeight="bold" mt={2}>
                    Transaction Successful
                </Typography>
            </Box>
            <Grid container spacing={2}>
                <Grid item xs={6}>
                    <Typography variant="body1" fontWeight="bold">
                        Attempt:
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1">{data.attempt}</Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1" fontWeight="bold">
                        ID:
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1">{data.id}</Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1" fontWeight="bold">
                        Request ID:
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1">{data.request_id}</Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1" fontWeight="bold">
                        Status:
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body1" color="success.main">
                        {data.status}
                    </Typography>
                </Grid>
            </Grid>
        </Paper>
    );
};

export default Receipt;

import {createTheme} from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: {
            main: '#01AEEE', // Primary color 0284C7
        },
        secondary: {
            main: '#dc004e', // Secondary color
        },
    },
    typography: {
        fontFamily: 'Roboto, Arial, sans-serif',
        fontSize: 16, // Base font size (default is 14)
        h4: {
            fontSize: '2rem', // Example for larger h4 headings
        },
        body1: {
            fontSize: '1.25rem', // Increase normal body text size
        },
        body2: {
            fontSize: '1.125rem', // Slightly smaller body text
        },
        h1: {
            fontSize: '2.5rem',
        },
    },
});

export default theme;

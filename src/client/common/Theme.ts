import { createMuiTheme } from "@material-ui/core/styles";

export const maskeraidTheme = createMuiTheme({
  palette: {
    primary: {
      light: "#515a66",
      main: "#363d46",
      dark: "#2B3038",
      contrastText: "white",
    },
    secondary: {
      main: "#64c3cc",
      light: "#8b94a0",
      dark: "#22293c",
    },
    background: {
      default: "#2B3038",
    },
    type: "dark",
  },
  spacing: 4,
  typography: {
    fontFamily: "sans-serif",
  },
});

import {
  createStyles,
  LinearProgress,
  Theme,
  withStyles,
  WithStyles,
} from "@material-ui/core";
import { blue } from "@material-ui/core/colors";
import { maskeraidTheme } from "../common/Theme";

export interface IMaskeraidPage extends WithStyles<typeof styles> {}

export const styles = (theme: Theme) =>
  createStyles({
    root: {
      backgroundColor: theme.palette.primary.contrastText,
    },
    tabOn: {
      backgroundColor: blue[800],
      height: "5px",
    },
    tabSelected: {
      fontSize: 12,
      backgroundColor: theme.palette.primary.dark,
      color: blue[800],
      //minWidth: "6vw",
      minWidth: "9vw",
    },
    tabNotSelected: {
      fontSize: 12,
      backgroundColor: theme.palette.primary.dark,
      //minWidth: "6vw",
      minWidth: "9vw",
    },
    tabContainer: {
      backgroundColor: theme.palette.primary.main,
      paddingBottom: theme.spacing(2),
    },
    tabs: {
      borderRadius: "20px",
      textAlign: "center",
    },
    tab: {
      fontSize: 20,
    },
    tabView: {
      color: theme.palette.primary.contrastText,
    },
    logo: {
      marginTop: theme.spacing(2),
      marginRight: theme.spacing(4),
      maxWidth: "80%",
      height: "auto",
    },
    button: {
      width: "10vw",
      margin: theme.spacing(2),
      marginRight: theme.spacing(0),
    },
    importButton: {
      marginRight: theme.spacing(5),
      width: "10vw",
      height: "auto",
      fontSize: 20,
    },
    inputImage: {
      width: "40vw",
    },
    gridContainer: {
      //height: "90vh",
      width: "100%",
      // background:
      //   "linear-gradient(180deg, rgba(255,255,255,0) 75%, rgba(0,183,255,1) 100%)",
    },
    inputContainer: {
      width: "40vw",
      height: "80vh",
      backgroundColor: theme.palette.secondary.light,
      position: "relative",
      marginTop: theme.spacing(10),
      boxShadow: "0px 10px 20px black",
    },
    generatedContainer: {
      width: "40vw",
      height: "80vh",
      backgroundColor: theme.palette.secondary.light,
      position: "relative",
      marginTop: theme.spacing(10),
      boxShadow: "0px 10px 20px black",
    },
    generateImageButton: {
      position: "absolute",
      width: "20vw",
      fontSize: 30,
      left: "50%",
      marginLeft: "-10vw",
      bottom: 0,
      marginBottom: theme.spacing(12),
      boxShadow: "0px 5px 10px black",
    },
  });

export const BorderLinearProgress = withStyles({
  root: {
    marginTop: maskeraidTheme.spacing(1),
    position: "absolute",
    height: 10,
    width: "10vw",
    backgroundColor: maskeraidTheme.palette.primary.contrastText,
    borderRadius: 20,
  },
  bar: {
    borderRadius: 20,
    backgroundColor: maskeraidTheme.palette.secondary.main,
  },
})(LinearProgress);

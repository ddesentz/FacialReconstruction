import { createStyles, Theme, WithStyles } from "@material-ui/core";
import { blue } from "@material-ui/core/colors";

export interface IHeader extends WithStyles<typeof styles> {
  rightItems?: React.ReactElement<JSX.Element>[];
  middleItems?: React.ReactElement<JSX.Element>[];
}

export const styles = (theme: Theme) =>
  createStyles({
    root: {
      //flexGrow: 1,
      position: "relative",
      backgroundColor: theme.palette.primary.main,
    },
    appBar: {
      height: "5vh",
      boxShadow: "0px 0px 35px black",
    },
    logo: {
      width: "10vw",
      marginLeft: theme.spacing(5),
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    statsContainer: {
      backgroundColor: theme.palette.secondary.dark,
      width: "100%",
      height: "15vh",
    },
    topStats: {
      fontSize: 28,
      backgroundColor: theme.palette.primary.dark,
    },
    title: {
      flexGrow: 1,
      width: "200px",
    },
    input: {
      display: "none",
    },
    icon: {
      margin: theme.spacing(2),
      color: theme.palette.secondary.dark,
      backgroundColor: theme.palette.primary.contrastText,
    },
    settingsContainer: {
      backgroundColor: theme.palette.primary.main,
      //padding: theme.spacing(1)
    },
    settingHeader: {
      fontSize: 28,
      textAlign: "center",
      padding: theme.spacing(2),
    },
    settingsOptionText: {
      fontSize: 18,
      textAlign: "center",
      padding: theme.spacing(2),
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
    drawer: {
      backgroundColor: theme.palette.primary.main,
      width: "18vw",
      position: "relative",
    },
    saveButton: {
      position: "absolute",
      bottom: 0,
      width: "18vw",
      left: "50%",
      marginLeft: "-9vw",
      //marginBottom: theme.spacing(4),
      textAlign: "center",
      fontSize: 20,
    },
    exportButton: {
      position: "absolute",
      bottom: "19vh",
      width: "16vw",
      left: "50%",
      marginLeft: "-8vw",
      marginBottom: theme.spacing(4),
    },
    deleteButton: {
      position: "absolute",
      bottom: "15vh",
      width: "16vw",
      left: "50%",
      marginLeft: "-8vw",
      marginBottom: theme.spacing(4),
      backgroundColor: theme.palette.info.main,
    },
    leftItems: {
      left: 0,
      position: "absolute",
      marginLeft: theme.spacing(2),
    },
    midItems: {
      width: "30vw",
      marginLeft: "-15vw",
      left: "50%",
      position: "absolute",
    },
    rightItems: {
      right: 0,
      position: "absolute",
      marginRight: theme.spacing(2),
    },
    tabView: {
      color: theme.palette.primary.contrastText,
    },
  });

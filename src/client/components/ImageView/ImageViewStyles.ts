import { createStyles, Theme, WithStyles } from "@material-ui/core";

export interface IImageView extends WithStyles<typeof styles> {
  title: string;
  src: string;
  name: string;
}

export const styles = (theme: Theme) =>
  createStyles({
    root: {
      //flexGrow: 1,
      position: "relative",
      backgroundColor: "transparent",
    },
    title: {
      margin: theme.spacing(4),
      backgroundColor: theme.palette.secondary.dark,
      color: theme.palette.primary.contrastText,
      padding: theme.spacing(3),
      boxShadow: "0px 0px 20px black",
    },
    srcImage: {
      textAlign: "center",
      position: "absolute",
      // backgroundColor: "transparent",
    },
    gridList: {
      width: "30vw",
      height: "70vh",
    },
    imageContainer: {
      width: "35vw !important",
      height: "70vh !important",
      backgroundColor: theme.palette.secondary.dark,
      position: "absolute",
      left: "50%",
      marginLeft: "-17.5vw",
      boxShadow: "0px 10px 20px black",
    },
    titleBar: {
      background:
        "linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(0,0,0,1) 100%)",
      height: theme.spacing(20),
      fontSize: "30 !important",
    },
    defaultIcon: {
      width: "35vw",
      height: "70vh",
    },
  });

import { createStyles, Theme, WithStyles } from '@material-ui/core';

export interface IMaskeraidPage extends WithStyles<typeof styles> {}

export const styles = (theme: Theme) =>
    createStyles({
        root: {
            backgroundColor: theme.palette.primary.contrastText,
        },
        logo: {
            marginTop: theme.spacing(2),
            marginRight: theme.spacing(4),
            maxWidth: "80%",
            height: "auto"
        },
        button: {
            width: "10vw",
            margin: theme.spacing(2),
            marginRight: theme.spacing(0)
        }
    });
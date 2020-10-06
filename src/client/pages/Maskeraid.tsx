import * as React from "react";
import {
    Button, Grid, Icon, Typography,
    withStyles,
} from "@material-ui/core";
import { observer } from "mobx-react";
import {IMaskeraidPage, styles} from "./MaskeraidStyles";
import logo from "../../maskeraidCentered.png"
import GetAppIcon from '@material-ui/icons/GetApp';
import axios from "axios";
import {TEST_ENDPOINT} from "../common/Endpoints";
import {stringify} from "querystring";

const MaskeraidComponent: React.FunctionComponent<IMaskeraidPage> = ({ classes }) => {
    const [displayData, setDisplayData] = React.useState(false);
    const [firstName, setFirstName] = React.useState("");
    const [lastName, setLastName] = React.useState("");
    const [path, setPath] = React.useState("");

    const handleAPI = () => {
        setDisplayData(true)
        axios.get(TEST_ENDPOINT).then(r => {
            setPath(r.data.result.fileName)
            setFirstName(r.data.result.FirstName)
            setLastName(r.data.result.LastName)
        })

    }

    return (
        <Grid container
              direction="column"
              justify="space-between"
              alignItems="center"
              className={classes.root}>
            <img src={logo} className={classes.logo}/>
            <Button
                variant="contained"
                color="primary"
                className={classes.button}
                startIcon={<GetAppIcon/>}
                onClick={handleAPI}
            >
                Test API Call
            </Button>
            {displayData && <Grid
                container
                direction="column"
                justify="space-between"
                alignItems="center"
            >
                <Typography>First Name: {firstName}</Typography>
                <Typography>Last Name: {lastName}</Typography>
                <Typography>Path: {path}</Typography>
            </Grid>}
        </Grid>
    );
};

export const MaskeraidPage = withStyles(styles)(observer(MaskeraidComponent));

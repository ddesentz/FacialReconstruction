import * as React from "react";
import {
  AppBar,
  Toolbar,
  withStyles,
  Grid,
  Tabs,
  Tab,
} from "@material-ui/core";

import { IHeader, styles } from "./HeaderStyles";
import { observer } from "mobx-react";
import logo from "../../../mASKerAId_Text.png";

const HeaderComponent: React.FunctionComponent<IHeader> = ({
  middleItems = [],
  rightItems = [],
  classes,
}) => {
  return (
    <div className={classes.root}>
      <AppBar position="static" className={classes.appBar}>
        <Toolbar>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="center"
          >
            <Grid item className={classes.leftItems}>
              <Grid
                container
                direction="row"
                justify="flex-start"
                alignItems="center"
              >
                <img src={logo} className={classes.logo} />
              </Grid>
            </Grid>
            <Grid item className={classes.midItems}>
              {middleItems.map((item, index) => (
                <div key={index}>{item}</div>
              ))}
            </Grid>
            <Grid item className={classes.rightItems}>
              <Grid
                container
                direction="row"
                justify="flex-end"
                alignItems="center"
              >
                {rightItems.map((item, index) => (
                  <div key={index}>{item}</div>
                ))}
              </Grid>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
};

export const Header = withStyles(styles)(observer(HeaderComponent));

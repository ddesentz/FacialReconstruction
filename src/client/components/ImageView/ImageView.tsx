import * as React from "react";
import {
  GridList,
  GridListTile,
  GridListTileBar,
  Typography,
  withStyles,
} from "@material-ui/core";
import { observer } from "mobx-react";
import { IImageView, styles } from "./ImageViewStyles";
import PersonIcon from "@material-ui/icons/Person";
import { API_ENDPOINT, GET_IMAGE } from "../../common/Endpoints";

const ImageViewComponent: React.FunctionComponent<IImageView> = ({
  title,
  src,
  name,
  type,
  classes,
}) => {
  const determineTitle = () => {
    if (name === "")
      return title.startsWith("Generated")
        ? "No Image Generated"
        : "No Image Selected";
    else return name;
  };

  const determineSrc = () => {
    if (type === "result") {
      return GET_IMAGE + src;
    } else return src;
  };

  return (
    <div className={classes.root}>
      <Typography align={"center"} variant={"h4"} className={classes.title}>
        {title}
      </Typography>
      <GridList className={classes.gridList} cols={1}>
        <GridListTile className={classes.imageContainer}>
          {name !== "" ? (
            <img
              id="input-image"
              src={determineSrc()}
              className={classes.srcImage}
              alt={""}
            />
          ) : (
            <PersonIcon className={classes.defaultIcon} />
          )}
          <GridListTileBar
            title={determineTitle()}
            className={classes.titleBar}
          />
        </GridListTile>
      </GridList>
    </div>
  );
};

export const ImageView = withStyles(styles)(observer(ImageViewComponent));

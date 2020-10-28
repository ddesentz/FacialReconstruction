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

const ImageViewComponent: React.FunctionComponent<IImageView> = ({
  title,
  src,
  name,
  classes,
}) => {
  const determineTitle = () => {
    if (src === "")
      return title.startsWith("Generated")
        ? "No Image Generated"
        : "No Image Selected";
    else return name;
  };

  return (
    <div className={classes.root}>
      <Typography align={"center"} variant={"h4"} className={classes.title}>
        {title}
      </Typography>
      <GridList className={classes.gridList} cols={1}>
        <GridListTile className={classes.imageContainer}>
          {src !== "" ? (
            <img
              id="input-image"
              src={src}
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

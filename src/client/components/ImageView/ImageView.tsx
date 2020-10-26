import * as React from "react";
import {
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
    if (src === "") return "No Image Selected";
    else return name;
  };

  return (
    <div className={classes.root}>
      <Typography align={"center"} variant={"h4"} className={classes.title}>
        {title}
      </Typography>
      <GridListTile key={src} className={classes.imageContainer}>
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
    </div>
  );
};

export const ImageView = withStyles(styles)(observer(ImageViewComponent));

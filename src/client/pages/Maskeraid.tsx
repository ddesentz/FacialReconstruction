import * as React from "react";
import {
  Button,
  Grid,
  Icon,
  Tab,
  Tabs,
  Typography,
  withStyles,
} from "@material-ui/core";
import { observer } from "mobx-react";
import { IMaskeraidPage, styles } from "./MaskeraidStyles";
import FolderIcon from "@material-ui/icons/Folder";
import { Header } from "../components/Header/Header";
import { ImageView } from "../components/ImageView/ImageView";

const MaskeraidComponent: React.FunctionComponent<IMaskeraidPage> = ({
  classes,
}) => {
  const [inputImage, setInputImage] = React.useState("");
  const [inputImageName, setInputImageName] = React.useState("");
  const [generatedImage, setGeneratedImage] = React.useState("");
  const inputFile = React.useRef(null);
  const algorithmRef = React.createRef();
  const [tabValue, setTabValue] = React.useState(0);

  const handleFileChange = (event: any) => {
    if (event.target.files && event.target.files[0]) {
      console.log(event.target.files[0].name);
      setInputImageName(event.target.files[0].name);
      setInputImage(URL.createObjectURL(event.target.files[0]));
    }
  };

  const BuildFileSelector = () =>
    React.createElement("input", {
      type: "file",
      accept: "image/gif, image/jpeg, image/png",
      ref: inputFile,
      style: { display: "none" },
      onChange: function (e) {
        handleFileChange(e);
      },
    });

  const handleImport = () => {
    // @ts-ignore
    inputFile.current.click();
  };

  const importButton = () => (
    <>
      <Button
        variant="contained"
        startIcon={<FolderIcon style={{ fontSize: 30 }} />}
        className={classes.importButton}
        onClick={handleImport}
      >
        Import Image
      </Button>
    </>
  );

  const handleTabChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setTabValue(newValue);
  };

  const selectAlgorithm = () => (
    <div>
      <Tabs
        value={tabValue}
        onChange={handleTabChange}
        classes={{ indicator: classes.tabOn }}
        className={classes.tabView}
        aria-label="disabled tabs example"
        centered
      >
        <Tab label="LBHP" />
        <Tab label="EIGEN" />
        <Tab label="FISHER" />
      </Tabs>
    </div>
  );

  const handleGenerate = () => {
    console.log("File Name: " + inputImageName);
    switch (tabValue) {
      case 0:
        return console.log("Algorithm: LBHP");
      case 1:
        return console.log("Algorithm: EIGEN");
      case 2:
        return console.log("Algorithm: FISHER");
    }
  };

  return (
    <>
      <Header middleItems={[selectAlgorithm()]} rightItems={[importButton()]} />
      <BuildFileSelector />
      <Grid
        container
        direction="row"
        justify="space-evenly"
        alignItems="flex-start"
        className={classes.gridContainer}
      >
        <Grid item className={classes.inputContainer}>
          <ImageView
            title={"Selected Image"}
            src={inputImage}
            name={inputImageName}
          />
        </Grid>
        <Grid item className={classes.generatedContainer}>
          <ImageView title={"Generated Image"} src={generatedImage} name={""} />
        </Grid>
      </Grid>
      <Button
        variant="contained"
        className={classes.generateImageButton}
        onClick={handleGenerate}
      >
        Generate Image
      </Button>
    </>
  );
};

export const MaskeraidPage = withStyles(styles)(observer(MaskeraidComponent));

import * as React from "react";
import {
  Button,
  Grid,
  LinearProgress,
  Tab,
  Tabs,
  withStyles,
} from "@material-ui/core";
import { observer } from "mobx-react";
import {
  BorderLinearProgress,
  IMaskeraidPage,
  styles,
} from "./MaskeraidStyles";
import FolderIcon from "@material-ui/icons/Folder";
import ImageIcon from "@material-ui/icons/Image";
import { Header } from "../components/Header/Header";
import { ImageView } from "../components/ImageView/ImageView";
import axios from "axios";
import {
  API_ENDPOINT,
  CLEAR_DB,
  ENROLL_DB,
  ENROLL_TEST,
  PREDICT,
} from "../common/Endpoints";
import { get, post } from "../common/HTTP";

const MaskeraidComponent: React.FunctionComponent<IMaskeraidPage> = ({
  classes,
}) => {
  const [inputImage, setInputImage] = React.useState("");
  const [inputImageName, setInputImageName] = React.useState("");
  const [predictImage, setPredictImage] = React.useState("");
  const [generatedImage, setGeneratedImage] = React.useState("");
  const [generatedImageName, setGeneratedImageName] = React.useState("");
  const inputFile = React.useRef(null);
  const inputDir = React.useRef(null);
  const [loading, setLoading] = React.useState(false);
  const [totalImages, setTotalImages] = React.useState(0);
  const [progress, setProgress] = React.useState(0);
  const [tabValue, setTabValue] = React.useState(0);

  const handleFileChange = (event: any) => {
    if (event.target.files && event.target.files[0]) {
      setInputImageName(event.target.files[0].name);
      setPredictImage(event.target.files[0]);
      setInputImage(URL.createObjectURL(event.target.files[0]));
    }
  };

  const handleDirChange = async (event: any) => {
    setLoading(true);
    const imagesDir = event.target.files;
    await axios.delete(CLEAR_DB);
    for (let i = 0; i < imagesDir.length; i++) {
      const formData = new FormData();
      console.log(imagesDir[i]);
      formData.append("img", imagesDir[i]);
      await axios({
        method: "POST",
        url: ENROLL_DB,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
          "Access-Control-Allow-Headers": "*",
        },
      }).then(() => {
        setProgress(i + 1);
      });
    }
    setLoading(false);
  };

  const BuildDirectorySelector = () =>
    React.createElement("input", {
      type: "file",
      multiple: "multiple",
      webkitdirectory: "true",
      ref: inputDir,
      style: { display: "none" },
      onChange: function (e) {
        handleDirChange(e);
      },
    });

  const BuildFileSelector = () =>
    React.createElement("input", {
      type: "file",
      accept: "*",
      ref: inputFile,
      style: { display: "none" },
      onChange: function (e) {
        handleFileChange(e);
      },
    });

  const handleImportFile = () => {
    // @ts-ignore
    inputFile.current.click();
  };

  const handleImportDir = () => {
    // @ts-ignore
    inputDir.current.click();
  };

  const importImageButton = () => (
    <>
      <Button
        variant="contained"
        startIcon={<ImageIcon style={{ fontSize: "2em" }} />}
        className={classes.importButton}
        onClick={handleImportFile}
      >
        Import Image
      </Button>
    </>
  );

  const importDirectoryButton = () => (
    <>
      <Button
        variant="contained"
        startIcon={<FolderIcon style={{ fontSize: "2em" }} />}
        className={classes.importButton}
        onClick={handleImportDir}
      >
        Import Database
      </Button>
      {loading && (
        <BorderLinearProgress
          variant="determinate"
          value={(progress / totalImages) * 100}
        />
      )}
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
        <Tab label="LBHP" className={classes.tab} />
        <Tab label="EIGEN" className={classes.tab} />
        <Tab label="FISHER" className={classes.tab} />
      </Tabs>
    </div>
  );

  const determineAlgorithm = () => {
    switch (tabValue) {
      case 0:
        return "LBHP";
      case 1:
        return "EIGHEN";
      case 2:
        return "FISHER";
    }
  };

  const handleGenerate = async () => {
    const formData = new FormData();
    formData.append("img", predictImage);
    await axios({
      method: "POST",
      url: ENROLL_TEST,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "*",
      },
    });
    post(PREDICT, {
      image: inputImageName,
      algorithm: determineAlgorithm(),
    }).then((data) => {
      Promise.resolve(data.json()).then((r) => {
        console.log(r.result);
        setGeneratedImageName(r.result);
      });
    });
  };

  return (
    <>
      <Header
        middleItems={[selectAlgorithm()]}
        rightItems={[importImageButton(), importDirectoryButton()]}
      />
      <BuildFileSelector />
      <BuildDirectorySelector />
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
            type={"input"}
          />
        </Grid>
        <Grid item className={classes.generatedContainer}>
          <ImageView
            title={"Generated Image"}
            src={generatedImageName}
            name={generatedImageName}
            type={"result"}
          />
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

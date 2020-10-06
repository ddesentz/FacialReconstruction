import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";
import { Provider } from "mobx-react";
import { ThemeProvider } from "@material-ui/styles";
import "reflect-metadata";
import {maskeraidTheme} from "./client/common/Theme";
import {defaultRootStore} from "./client/stores/RootStore";
import { AppContext } from "./client/common/AppContext";

const store = defaultRootStore({});

ReactDOM.render(
    <Provider rootstore={store} {...store}>
        <AppContext.Provider value={store}>
            <ThemeProvider theme={maskeraidTheme}>
                <App />
            </ThemeProvider>
        </AppContext.Provider>
    </Provider>,
    document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

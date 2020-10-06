import * as React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "reflect-metadata";
import {MaskeraidPage} from "./client/pages/Maskeraid";

class App extends React.Component {
  render() {
    return (
        <React.Fragment>
          <Router>
            <Switch>
              <Route
                  exact={true}
                  path="/"
                  title="ANDDE"
                  render={() => <MaskeraidPage />}
              />
            </Switch>
          </Router>
        </React.Fragment>
    );
  }
}

export default App;

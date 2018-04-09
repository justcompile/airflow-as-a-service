import React, { Component } from 'react';
import {Route, Switch, BrowserRouter} from 'react-router-dom';

import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import baseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import airflowAsAServiceApp from "./reducers";

import RepoList from "./components/RepoList";
import Clusters from "./components/Clusters";
import NotFound from "./components/NotFound";

let store = createStore(airflowAsAServiceApp, applyMiddleware(thunk));

const muiTheme = getMuiTheme(baseTheme);
  

class App extends Component {
    render() {
        return (
            <MuiThemeProvider muiTheme={muiTheme}>
                <Provider store={store}>
                    <BrowserRouter>
                        <Switch>
                            <Route exact path="/" component={Clusters} />
                            <Route exact path="/repos" component={RepoList} />
                            <Route component={NotFound} />
                        </Switch>
                    </BrowserRouter>
                </Provider>
            </MuiThemeProvider>
        );
    }
}

export default App;

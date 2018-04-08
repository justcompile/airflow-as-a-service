import React, { Component } from 'react';
import {Route, Switch, BrowserRouter} from 'react-router-dom';

import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import airflowAsAServiceApp from "./reducers";

import RepoList from "./components/RepoList";
import Clusters from "./components/Clusters";
import NotFound from "./components/NotFound";

let store = createStore(airflowAsAServiceApp, applyMiddleware(thunk));

class App extends Component {
    render() {
        return (
            <Provider store={store}>
                <BrowserRouter>
                    <Switch>
                        <Route exact path="/" component={Clusters} />
                        <Route exact path="/repos" component={RepoList} />
                        <Route component={NotFound} />
                    </Switch>
                </BrowserRouter>
            </Provider>
        );
    }
}

export default App;

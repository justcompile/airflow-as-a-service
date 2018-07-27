import React, { Component } from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import airflowAsAServiceApp from "./reducers";

// Navigation Components
import SideNav from "./components/SideNav";
import TopBar from "./components/TopBar";

// Page Components
import BuildList from "./components/BuildList";
import Cluster from "./components/Cluster";
import ClusterList from "./components/ClusterList";
import NotFound from "./components/NotFound";
import Plans from "./components/Plans";
import RepoList from "./components/RepoList";

let store = createStore(airflowAsAServiceApp, applyMiddleware(thunk));

const defaultTheme = createMuiTheme();

const styles = theme => ({
    root: {
        flexGrow: 1,
        zIndex: 1,
        overflow: 'hidden',
        position: 'relative',
        display: 'flex',
    },
    toolbar: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: '0 8px',
        ...theme.mixins.toolbar,
    },
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing.unit * 3,
    },
});


class App extends Component {
    constructor(props) {
        super(props);
        this.handleNavigationToggle = this.handleNavigationToggle.bind(this);
        this.state = { open: false };
    }

    handleNavigationToggle(value) {
        this.setState({ open: value })
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root}>
                <MuiThemeProvider theme={defaultTheme}>
                    <Provider store={store}>
                        <BrowserRouter>
                            <React.Fragment>
                            <TopBar open={this.state.open} onToggleDrawer={this.handleNavigationToggle} />
                            <SideNav open={this.state.open} onToggleDrawer={this.handleNavigationToggle} />
                            <main className={classes.content}>
                                <div className={classes.toolbar} />
                                
                                    <Switch>
                                        <Route exact path="/" component={ClusterList} />
                                        <Route exact path="/builds" component={BuildList} />
                                        <Route path="/cluster/:clusterId" component={Cluster} />
                                        <Route exact path="/repos" component={RepoList} />
                                        <Route exact path="/plans" component={Plans} />
                                        <Route component={NotFound} />
                                    </Switch>
                            </main>
                            </React.Fragment>
                        </BrowserRouter>
                    </Provider>
                </MuiThemeProvider>
            </div>
        );
    }
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(App);


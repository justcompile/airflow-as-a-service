import React, { Component } from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import { MuiThemeProvider, createMuiTheme } from 'material-ui/styles';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import airflowAsAServiceApp from "./reducers";

// Navigation Components
import SideNav from "./components/SideNav";
import TopBar from "./components/TopBar";

// Page Components
import RepoList from "./components/RepoList";
import Clusters from "./components/Clusters";
import NotFound from "./components/NotFound";

let store = createStore(airflowAsAServiceApp, applyMiddleware(thunk));

const defaultTheme = createMuiTheme();

const styles = theme => ({
    root: {
        flexGrow: 1,
        height: 430,
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
                    <TopBar open={this.state.open} onToggleDrawer={this.handleNavigationToggle} />
                    <SideNav open={this.state.open} onToggleDrawer={this.handleNavigationToggle} />
                    <main className={classes.content}>
                        <div className={classes.toolbar} />
                        <Provider store={store}>
                            <BrowserRouter>
                                <Switch>
                                    <Route exact path="/" component={Clusters} />
                                    <Route exact path="/repos" component={RepoList} />
                                    <Route component={NotFound} />
                                </Switch>
                            </BrowserRouter>
                        </Provider>
                    </main>
                </MuiThemeProvider>
            </div>
        );
    }
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(App);


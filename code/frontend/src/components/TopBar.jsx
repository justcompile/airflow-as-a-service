import React, { Component } from 'react';

import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

const drawerWidth = 240;

const styles = theme => ({
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    menuButton: {
        marginLeft: 12,
        marginRight: 36,
    },
    hide: {
        display: 'none',
    },
});


class TopBar extends Component {
    constructor(props) {
        super(props)
        this.drawStateChange = this.drawStateChange.bind(this);
    }

    drawStateChange(value) {
        this.props.onToggleDrawer(value);
    }

    handleDrawerOpen = () => {
        //this.setState({ open: true });
        this.drawStateChange(true)
    };


    render() {
        const { classes, open } = this.props;
        return (
            <AppBar
                position="absolute"
                className={classNames(classes.appBar, open && classes.appBarShift)}>
                <Toolbar disableGutters={!open}>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        onClick={this.handleDrawerOpen}
                        className={classNames(classes.menuButton, open && classes.hide)}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="title" color="inherit" noWrap>
                        Airflow as a Service
                    </Typography>
                </Toolbar>
            </AppBar>
        );
    }
}

TopBar.propTypes = {
    classes: PropTypes.object.isRequired,
    open: PropTypes.bool,
    onToggleDrawer: PropTypes.func,
};


export default withStyles(styles, { withTheme: true })(TopBar);

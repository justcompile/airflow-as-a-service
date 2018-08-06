import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import CloseIcon from '@material-ui/icons/Close';
import ErrorIcon from '@material-ui/icons/Error';
import IconButton from '@material-ui/core/IconButton';
import Snackbar from '@material-ui/core/Snackbar';
import SnackbarContent from '@material-ui/core/SnackbarContent';
import { withStyles } from '@material-ui/core/styles';

import {connect} from 'react-redux';
import {errors} from "../../actions";

const variantIcon = {
  error: ErrorIcon,
};

const styles = theme => ({
  margin: {
    margin: theme.spacing.unit,
  },
  error: {
    backgroundColor: theme.palette.error.dark,
  },
  icon: {
    fontSize: 20,
  },
  iconVariant: {
    opacity: 0.9,
    marginRight: theme.spacing.unit,
  },
  message: {
    display: 'flex',
    alignItems: 'center',
  },
});

class ErrorBar extends React.Component {
    defaultState = {
        open: false,
    }

    constructor(props) {
        super(props)
        this.state = this.defaultState
    }

    handleClose = (event, reason) => {
        this.props.clear();
        if (reason === 'clickaway') {
          return;
        }
    
        this.setState({ open: false });
    };

    render() {
        const { classes } = this.props;
        const Icon = variantIcon.error;
        console.log(this.props)
        const open = this.props.error.message !== undefined;

        return (
            <Snackbar
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
                open={open}
                autoHideDuration={6000}
                onClose={this.handleClose}
                >
                    <SnackbarContent
                        className={classNames(classes.error, classes.margin)}
                        aria-describedby="client-snackbar"
                        message={
                            <span id="client-snackbar" className={classes.message}>
                            <Icon className={classNames(classes.icon, classes.iconVariant)} />
                            {this.props.error.message}
                            </span>
                        }
                        action={[
                            <IconButton
                            key="close"
                            aria-label="Close"
                            color="inherit"
                            className={classes.close}
                            onClick={this.handleClose}
                            >
                            <CloseIcon className={classes.icon} />
                            </IconButton>,
                        ]} />
            </Snackbar>
        );
    }
}

const mapStateToProps = state => {
    return {
        error: state.errors,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        clear: () => {
            dispatch(errors.clear());
        },
    }
}

ErrorBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(ErrorBar));

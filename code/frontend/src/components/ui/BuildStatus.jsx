import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';

const styles = theme => ({
    button: {
        margin: theme.spacing.unit,
        width: 130,
        "&:hover": {
            backgroundColor: theme.palette.grey[300],
            cursor: 'default'
        },
        cursor: 'default'
    },
    rightIcon: {
        marginLeft: theme.spacing.unit,
    },
  });


class BuildStatus extends Component {
    render() {
        const { currentStatus, classes } = this.props;

        return (
            <div>
                <Button variant="contained" color="default" className={classes.button}>
                    {currentStatus.toUpperCase()}
                </Button>
            </div>
        )
    }
}

BuildStatus.propTypes = {
    classes: PropTypes.object.isRequired,
    currentStatus: PropTypes.string.isRequired,
};


export default withStyles(styles)(BuildStatus);

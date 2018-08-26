import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';

import Avatar from '@material-ui/core/Avatar';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

import ButtonMenu from './ui/ButtonMenu';


import {connect} from 'react-redux';

import {builds} from "../actions";

const styles = theme => ({
    root: {
      overflow: 'hidden',
      padding: `0 ${theme.spacing.unit * 3}px`,
    },
    wrapper: {
      maxWidth: 400,
    },
    paper: {
      margin: theme.spacing.unit,
      padding: theme.spacing.unit * 2,
    },
    gitlink: {
        color: theme.palette.text.secondary,
        cursor: 'pointer',
        'text-decoration': 'none',
    },
    statusButton: {
        "&:hover": {
            backgroundColor: "transparent",
            cursor: 'default'
        }
    },
    queuedStatus: {
        backgroundColor: theme.palette.background.paper,
    },
    runningStatus: {
        backgroundColor: theme.palette.background.paper,
    },
    successStatus: {
        backgroundColor: "#52d869",
        color: theme.palette.common.white,
    },
    failedStatus: {
        backgroundColor: theme.palette.error.dark,
    },
    stoppedStatus: {
        backgroundColor: "#ffa154",
    },
  });

class BuildListItem extends Component {
    triggerBuildStatusChange = () => {
        this.props.updateBuildStatus(this.props.build);
    }

    render() {
        const { classes, build } = this.props

        return (
            <Paper className={`${classes.paper} ${classes[build.status.toLowerCase()+'Status']}`}>
                <Grid container wrap="nowrap" spacing={16}>
                    <Grid item>
                    <Avatar alt={`Commited by ${build.committer}`} src={`https://github.com/${build.committer}.png`} />
                    </Grid>
                    <Grid item sm={10} zeroMinWidth>
                    <Typography noWrap>{build.message}</Typography>
                    <Typography variant="caption">
                        <a className={classes.gitlink} href={`${build.repository.url}/${build.commit_id}`} target="_blank">{build.commit_id}</a>
                    </Typography>
                    </Grid>
                    <Grid item container direction="column" justify="center" alignItems="center" sm={2}>
                        <ButtonMenu currentStatus={build.status} onSelect={this.triggerBuildStatusChange} />
                    </Grid>
                </Grid>
            </Paper>
        )
    }
}


const mapStateToProps = state => {
    return {}
}

const mapDispatchToProps = dispatch => {
    return {
        updateBuildStatus: (build) => {
            dispatch(builds.updateBuildStatus(build));
        },
    }
}

BuildListItem.propTypes = {
    classes: PropTypes.object.isRequired,
    build: PropTypes.object.isRequired,
};


export default withStyles(styles)(withRouter(connect(mapStateToProps, mapDispatchToProps)(BuildListItem)));


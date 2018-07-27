import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';

import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

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
  });

class BuildList extends Component {
    componentDidMount() {
        this.props.fetchBuilds()
    }

    render() {
        const { classes } = this.props

        return (
            <div>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">Builds</Typography>
                    </Grid>
                </Grid>
                <div>
                    {this.props.builds.map((build, id) => (
                    <Paper className={classes.paper} key={`build_${build.id}`}>
                        <Grid container wrap="nowrap" spacing={16}>
                          <Grid item xs zeroMinWidth>
                            <Typography noWrap>{build.commit_id}</Typography>
                            <Typography variant="caption">{build.status}</Typography>
                          </Grid>
                        </Grid>
                    </Paper>
                ))}
                </div>
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        builds: state.builds,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchBuilds: () => {
            dispatch(builds.fetchBuilds());
        },
    }
}

BuildList.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(withRouter(connect(mapStateToProps, mapDispatchToProps)(BuildList)));


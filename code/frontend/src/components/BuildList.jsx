import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';

import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
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
    gitlink: {
        color: theme.palette.text.secondary,
        cursor: 'pointer',
        'text-decoration': 'none',
    },
    statusButton: {
        "&:hover": {
            "background-color": 'transparent',
            cursor: 'default'
        }
    }
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
                          <Grid item>
                            <Avatar alt={`Commited by ${build.committer}`} src={`https://github.com/${build.committer}.png`} />
                          </Grid>
                          <Grid item sm={11} zeroMinWidth>
                            <Typography noWrap>{build.message}</Typography>
                            <Typography variant="caption">
                                <a className={classes.gitlink} href={`${build.repository.repo_url}/${build.commit_id}`} target="_blank">{build.commit_id}</a>
                            </Typography>
                          </Grid>
                          <Grid item container direction="column" justify="center" alignItems="center" sm={1}>
                            <Button className={classes.statusButton}>{build.status}</Button>
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


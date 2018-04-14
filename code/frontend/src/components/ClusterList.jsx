import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { withRouter } from 'react-router-dom';

import Avatar from 'material-ui/Avatar';
import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';

import {connect} from 'react-redux';

import {clusters} from "../actions";

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

class ClusterList extends Component {
    defaultState = { creating: false, intervalId: null }

    constructor(props) {
        super(props)
        this.state = this.defaultState
    }

    componentDidMount() {
        this.props.fetchClusters()
    }

    componentWillUnmount() {
        if (this.state.intervalId) {
            this.stopPolling()
        }
    }

    stopPolling() {
        clearInterval(this.state.intervalId);
        this.setState({ ...this.defaultState })
    }

    pollUntilRunning() {
        const self = this
        if (!this.state.creating) {
            const intervalId = setInterval(() => {
                if (self.props.clusters.filter(cluster => cluster.status !== 'running').length) {
                    self.props.fetchClusters()
                } else {
                    self.stopPolling()
                }
            }, 5000);

            self.setState({creating: true, intervalId})
        }
    }

    createCluster = (e) => {
        e.preventDefault();
        this.props.addCluster();
        this.pollUntilRunning();
    }

    deleteCluster = (clusterId, e) => {
        e.preventDefault();
        console.log(clusterId);
        if (this.state.creating && this.props.clusters.length <= 1) {
            this.stopPolling();
        }
        this.props.deleteCluster(clusterId);
    }

    openCluster(clusterId) {
        this.props.history.push(`/cluster/${clusterId}`)
    }

    render() {
        const { classes } = this.props

        return (
            <div>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">Clusters</Typography>
                    </Grid>
                    <Grid item>
                        <Button disabled={this.props.clusters.length >= 5} variant="raised" color="primary" onClick={this.createCluster}>Create Cluster</Button>
                    </Grid>
                </Grid>

                <div>
                    {this.props.clusters.map((cluster, id) => (
                    <Paper className={classes.paper} key={`cluster_${cluster.id}`}>
                        <Grid container wrap="nowrap" spacing={16}>
                          <Grid item onClick={() => this.openCluster(cluster.id)}>
                            <Avatar>{cluster.name[0].toUpperCase()}</Avatar>
                          </Grid>
                          <Grid item xs zeroMinWidth onClick={() => this.openCluster(cluster.id)}>
                            <Typography noWrap>{cluster.name}</Typography>
                            <Typography variant="caption">{cluster.status}</Typography>
                          </Grid>
                          <Grid item>
                            <IconButton aria-label="Delete" onClick={(evt) => this.deleteCluster(cluster.id, evt)}>
                                <DeleteIcon />
                            </IconButton>
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
        clusters: state.clusters,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchClusters: () => {
            dispatch(clusters.fetchClusters());
        },
        addCluster: () => {
            dispatch(clusters.addCluster());
        },
        deleteCluster: (clusterId) => {
            dispatch(clusters.deleteCluster(clusterId));
        },
    }
}

ClusterList.propTypes = {
    classes: PropTypes.object.isRequired,
    history: PropTypes.shape({
        push: PropTypes.func.isRequired,
    })
};


export default withStyles(styles)(withRouter(connect(mapStateToProps, mapDispatchToProps)(ClusterList)));


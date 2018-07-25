import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';

import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';

import {connect} from 'react-redux';

import {clusters} from "../actions";
import ClusterCreateDialog from "./dialogs/CreateCluster";

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
    defaultState = { creating: false, intervalId: null, open: false }

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
        this.setState({open: true});
    }

    modalCancel = () => {
        this.setState({open: false});
    }

    modalSubmit = (params) => {
        this.props.addCluster(params);
        this.pollUntilRunning();
        this.setState({open: false});
    }

    deleteCluster = (clusterId, e) => {
        e.preventDefault();

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
                <ClusterCreateDialog open={this.state.open} onCancel={this.modalCancel} onSubmit={this.modalSubmit} />
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
        addCluster: (params) => {
            dispatch(clusters.addCluster(params));
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


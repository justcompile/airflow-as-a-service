import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import Avatar from 'material-ui/Avatar';
import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

import {connect} from 'react-redux';

import {clusters} from "../actions";

import ClusterEvents from "./ClusterEvents";


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

class Cluster extends Component {
    constructor(props) {
        super(props)
        this.state = this.defaultState
    }

    componentDidMount() {
        this.props.fetchCluster(this.props.match.params.clusterId)
    }

    openUI(endpoint) {
        window.open(endpoint, '_blank');
    }

    render() {
        const { classes } = this.props

        if (!this.props.cluster) {
            return ( <div></div> )
        }

        const cluster = this.props.cluster;
        console.dir(cluster);
        return (
            <div>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">{cluster.name}</Typography>
                    </Grid>
                </Grid>

                <div>
                <Paper className={classes.paper} key={`cluster_${cluster.id}`}>
                    <Grid container wrap="nowrap" spacing={16}>
                        <Grid item>
                            <Avatar>{cluster.name[0].toUpperCase()}</Avatar>
                        </Grid>
                        <Grid item xs zeroMinWidth>
                            <Typography noWrap>{cluster.name}</Typography>
                            <Typography variant="caption">{cluster.status}</Typography>
                        </Grid>
                        <Grid item>
                            <Button variant="raised" color="primary" onClick={() => this.openUI(cluster.ui_endpoint)}>View UI</Button>
                          </Grid>
                    </Grid>
                    <div>
                        <h3>Details</h3>
                        <dl>
                            <dt>Airflow MetaDB</dt>
                            <dd>{cluster.db_instance.varient}: {cluster.db_instance.version}</dd>
                        </dl>
                    </div>
                </Paper>
                <ClusterEvents clusterId={cluster.id} />
                </div>
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        cluster: state.cluster,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchCluster: (clusterId) => {
            dispatch(clusters.fetchCluster(clusterId));
        },
    }
}

Cluster.propTypes = {
    classes: PropTypes.object.isRequired,
    match: PropTypes.object.isRequired,
};


export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(Cluster));


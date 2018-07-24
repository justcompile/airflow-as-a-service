import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

// import Avatar from 'material-ui/Avatar';
// import Button from 'material-ui/Button';
import Grid from '@material-ui/core/Grid';
// import Paper from 'material-ui/Paper';
import Typography from '@material-ui/core/Typography';

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

class ClusterEvents extends Component {
    defaultState = { intervalId: null }

    constructor(props) {
        super(props)
        this.state = this.defaultState
    }

    componentDidMount() {
        this.props.fetchClusterEvents(this.props.clusterId)
        this.startPolling()
    }

    componentWillUnmount() {
        if (this.state.intervalId) {
            this.stopPolling()
        }
    }

    startPolling() {
        const self = this
        if (!this.state.intervalId) {
            const intervalId = setInterval(() => {
                self.props.fetchClusterEvents(self.props.clusterId)
            }, 5000);

            self.setState({creating: true, intervalId})
        }
    }

    stopPolling() {
        clearInterval(this.state.intervalId);
        this.setState({ ...this.defaultState })
    }

    render() {
        if (!this.props.events) {
            return ( <div></div> )
        }
        return (
            <div>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">Events</Typography>
                    </Grid>
                </Grid>

                <div>
                    <ul>
                    {this.props.events.map((clusterEvent, id) => (
                        <li key={clusterEvent.id}><span>{clusterEvent.description || clusterEvent.event_type} | {clusterEvent.created_at}</span></li>
                    ))}
                    </ul>
                </div>
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        events: state.clusterEvents,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchClusterEvents: (clusterId) => {
            dispatch(clusters.fetchClusterEvents(clusterId));
        },
    }
}

ClusterEvents.propTypes = {
    classes: PropTypes.object.isRequired,
    clusterId: PropTypes.string.isRequired,
};


export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(ClusterEvents));


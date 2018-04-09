import React, { Component } from 'react';
import RaisedButton from 'material-ui/FlatButton';
import {connect} from 'react-redux';
import muiThemeable from 'material-ui/styles/muiThemeable';

import {clusters} from "../actions";


class Clusters extends Component {
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

    render() {
        return (
            <div>
                <h2>Clusters</h2>
                <div>
                    <ul>
                    {this.props.clusters.map((cluster, id) => (
                    <li key={`cluster_${cluster.id}`}>
                        {cluster.name} - {cluster.status}
                    </li>
                ))}
                </ul>
                </div>
                <RaisedButton primary={true} onClick={this.createCluster} label="Create Cluster" />
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
    }
}


export default muiThemeable()(connect(mapStateToProps, mapDispatchToProps)(Clusters));


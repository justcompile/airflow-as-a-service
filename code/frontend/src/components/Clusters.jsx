import React, { Component } from 'react';
import {connect} from 'react-redux';

import {clusters} from "../actions";


class Clusters extends Component {
    componentDidMount() {
        this.props.fetchClusters();
    }

    createCluster = (e) => {
        e.preventDefault();
        this.props.addCluster();
    }

    render() {
        return (
            <div>
                <h2>Clusters</h2>
                <div>
                    <ul>
                    {this.props.clusters.map((cluster, id) => (
                    <li key={`note_${cluster.id}`}>
                        {cluster.name} - {cluster.status}
                    </li>
                ))}
                </ul>
                </div>
                <button onClick={this.createCluster}>Create Cluster</button>
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


export default connect(mapStateToProps, mapDispatchToProps)(Clusters);


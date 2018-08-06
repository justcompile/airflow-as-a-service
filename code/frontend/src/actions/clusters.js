import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient()


export const fetchClusters = () => {
    return dispatch => {
        return client.list('clusters')
            .then(clusters => {
                return dispatch({
                    type: 'FETCH_CLUSTERS',
                    clusters
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}

export const fetchCluster = (clusterId) => {
    return dispatch => {
        return client.get('clusters', clusterId)
            .then(cluster => {
                return dispatch({
                    type: 'FETCH_CLUSTER',
                    cluster
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}

export const fetchClusterEvents = (clusterId) => {
    return dispatch => {
        return client.getChild('clusters', clusterId, 'events')
            .then(clusterEvents => {
                return dispatch({
                    type: 'FETCH_CLUSTER_EVENTS',
                    events: clusterEvents
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}

export const addCluster = (params) => {
    return dispatch => {
        return client.create('clusters', {...params})
            .then(cluster => {
                return dispatch({
                    type: 'ADD_CLUSTER',
                    cluster
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}


export const deleteCluster = (clusterId) => {
    return dispatch => {
      return client.delete('clusters', clusterId)
        .then(res => {
            return dispatch({
                type: 'DELETE_CLUSTER',
                clusterId
            })
        })
        .catch((error) => errorHandler(dispatch, error));
    }
}

export const fetchDBTypes = () => {
    return dispatch => {
        return client.list('dbs')
            .then(dbTypes => {
                return dispatch({
                    type: 'FETCH_DB_TYPES',
                    dbTypes
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}


export const connectToSocket = () => {
    return dispatch => {
        return dispatch({
            type: 'WEBSOCKET/REQUEST/OPEN',
            payload: {
                id: 'clusters',
                url: 'ws://localhost:8000/ws/clusters/'
            }
        })
    }      
}

export const disconnect = () => {
    return dispatch => {
        return dispatch({
            type: 'WEBSOCKET/REQUEST/CLOSE',
            payload: {
                id: 'clusters',
                url: 'ws://localhost:8000/ws/clusters/'
            }
        })
    }
}
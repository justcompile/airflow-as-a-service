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
    }
}

export const addCluster = () => {
    return dispatch => {
        return client.create('clusters', {})
            .then(cluster => {
                return dispatch({
                    type: 'ADD_CLUSTER',
                    cluster
                })
            })
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
    }
}

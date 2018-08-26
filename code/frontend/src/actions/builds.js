import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient();

const statusWorkflow = {
    "STOPPED": "QUEUED",
    "QUEUED": "RUNNING",
    "RUNNING": "STOPPED",
    "FAILED": "QUEUED",
    "SUCCESS": "QUEUED",
}

const getNextStatus = (currentStatus) => {
    return statusWorkflow[currentStatus.toUpperCase()].toLowerCase();
};

export const fetchBuilds = () => {
    return dispatch => {
        return client.list('builds')
            .then(builds => {
                return dispatch({
                    type: 'FETCH_BUILDS',
                    builds
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}

export const updateBuildStatus = (build) => {
    return dispatch => {
        return client.update('builds', build.id, {status: getNextStatus(build.status)})
            // .then(builds => {
            //     return dispatch({
            //         type: 'FETCH_BUILDS',
            //         builds
            //     })
            // })
            .catch((error) => errorHandler(dispatch, error));
    }
}

export const connectToSocket = () => {
    return dispatch => {
        return dispatch({
            type: 'WEBSOCKET/REQUEST/OPEN',
            payload: {
                id: 'builds',
                url: 'ws://localhost:8000/ws/builds/'
            }
        })
    }      
}

export const disconnect = () => {
    return dispatch => {
        return dispatch({
            type: 'WEBSOCKET/REQUEST/CLOSE',
            payload: {
                id: 'builds',
                url: 'ws://localhost:8000/ws/builds/'
            }
        })
    }
}
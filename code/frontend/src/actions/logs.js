import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient();


export const getBuildLog = (buildId) => {
    return dispatch => {
        return client.getChild('builds', buildId, 'log')
            .then(log => {
                return dispatch({
                    type: 'FETCH_LOG',
                    log
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}


export const connectToSocket = (buildId) => {
    return dispatch => {
        return dispatch({
            type: 'WEBSOCKET/REQUEST/OPEN',
            payload: {
                id: 'buildLog',
                url: `ws://localhost:8000/ws/builds/${buildId}/log/`
            }
        })
    }      
}

export const disconnect = (buildId) => {
    return dispatch => {
        return dispatch({
            type: 'WEBSOCKET/REQUEST/CLOSE',
            payload: {
                id: 'buildLog',
                url: `ws://localhost:8000/ws/builds/${buildId}/log/`
            }
        })
    }
}
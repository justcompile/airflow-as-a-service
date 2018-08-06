import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient()

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
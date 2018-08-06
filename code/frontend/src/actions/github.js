import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient()

export const fetchRemoteRepos = () => {
    return dispatch => {
        return client.list('github')
            .then(repos => {
                return dispatch({
                    type: 'FETCH_REMOTE_REPOS',
                    repos
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}

export const addRepo = (repo) => {
    return dispatch => {
        return client.create('github', {repo})
            .then(repo => {
                return dispatch({
                    type: 'ADD_REPO',
                    repo
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}


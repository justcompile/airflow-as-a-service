import ApiClient from '../api'

const client = new ApiClient()

export const fetchUserRepos = () => {
    return dispatch => {
        return client.list('repositories')
            .then(repos => {
                return dispatch({
                    type: 'FETCH_USER_REPOS',
                    repos
                })
            })
    }
}
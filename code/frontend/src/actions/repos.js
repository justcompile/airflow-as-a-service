import ApiClient from '../api'

const client = new ApiClient()

export const fetchRepos = () => {
    return dispatch => {
        return client.list('github')
            .then(repos => {
                return dispatch({
                    type: 'FETCH_REPOS',
                    repos
                })
            })
    }
}

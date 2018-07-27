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
    }
}

export const fetchRepos = () => {
    return dispatch => {
        let headers = {"Content-Type": "application/json"};
        return fetch("/api/github/", {headers, credentials: 'include'})
            .then(res => res.json())
            .then(repos => {
                return dispatch({
                    type: 'FETCH_REPOS',
                    repos
                })
            })
    }
}

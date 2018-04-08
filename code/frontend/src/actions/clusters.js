const trim = (text) => {
    return text == null ?
        "" :
        ( text + "" ).replace( /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "" );
}

const getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


export const fetchClusters = () => {
    return dispatch => {
        let headers = {"Content-Type": "application/json", 'X-CSRFToken': getCookie('csrftoken')};
        return fetch("/api/clusters/", {headers, credentials: 'include'})
            .then(res => res.json())
            .then(clusters => {
                return dispatch({
                    type: 'FETCH_CLUSTERS',
                    clusters
                })
            })
    }
}

export const addCluster = () => {
    return dispatch => {
      let headers = {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')};

      return fetch("/api/clusters/", {credentials: 'include', headers, method: "POST", body: {}})
        .then(res => res.json())
        .then(cluster => {
          return dispatch({
            type: 'ADD_CLUSTER',
            cluster
          })
        })
    }
}

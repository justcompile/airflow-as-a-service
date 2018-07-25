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


class ApiClient {
    constructor() {
        this.defaultHeaders = { "Content-Type": "application/json", 'X-CSRFToken': getCookie('csrftoken') }
    }

    create(entity, body) {
        return fetch(`/api/${entity}/`, { ...this._defaultRequestParams(), method: "POST", body: JSON.stringify(body) })
            .then(res => res.json())
    }

    delete(entity, id) {
        return fetch(`/api/${entity}/${id}/`, { ...this._defaultRequestParams(), method: "DELETE" })
    }

    get(entity, id) {
        return fetch(`/api/${entity}/${id}/`, { ...this._defaultRequestParams() })
            .then(res => res.json())
    }

    getChild(entity, id, childEntity) {
        return fetch(`/api/${entity}/${id}/${childEntity}/`, { ...this._defaultRequestParams() })
            .then(res => res.json())
    }

    list(entity) {
        return fetch(`/api/${entity}/`, { ...this._defaultRequestParams() })
            .then(res => res.json())
    }

    raw(endpoint, method, body) {
        return fetch(endpoint, { ...this._defaultRequestParams(), method , body: JSON.stringify(body) })
            .then(res => res.json())
    }

    _defaultRequestParams() {
        return {
            credentials: 'include', headers: this.defaultHeaders
        }
    }
}

export default ApiClient
const initialState = [];


export default function clusters(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_CLUSTERS':
            return [...action.clusters];
        
        case 'ADD_CLUSTER':
            return [...state, action.cluster];

        case 'DELETE_CLUSTER':
            return [...state.filter(item => action.clusterId !== item.id)];

        case 'WEBSOCKET/EVENT/MESSAGE':
            if (action.payload.id === 'clusters') {
                const cluster = JSON.parse(action.payload.event.data).message;

                const clone = [...state];
                clone[clone.findIndex(element => element.id === cluster.id)] = cluster;
                return clone;
            }

            return state;

        default:
            return state;
    }
}

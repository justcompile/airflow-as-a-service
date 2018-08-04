const initialState = [];


export default function builds(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_BUILDS':
            return [...action.builds];

        case 'WEBSOCKET/EVENT/MESSAGE':
            console.log('got a message...')
            if (action.payload.id === 'builds') {
                const build = JSON.parse(action.payload.event.data).message;

                const clone = [...state];
                console.log('state before: ', state);
                clone[clone.findIndex(element => element.id === build.id)] = build;
                console.log('state after: ', clone);
                return clone;
            }

            return state;
        
        default:
            return state;
    }
}

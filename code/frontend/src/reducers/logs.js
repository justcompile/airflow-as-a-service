import { updateStateFromSocket } from './helpers';

const initialState = [];


export default function logs(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_LOG':
            return {...action.log};

        case 'WEBSOCKET/EVENT/MESSAGE':
            return updateStateFromSocket('buildLog', state, action);
        
        default:
            return state;
    }
}

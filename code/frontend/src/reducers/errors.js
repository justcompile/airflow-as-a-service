import { updateFromSocket } from './helpers';

const initialState = {};


export default function errors(state=initialState, action) {
    switch (action.type) {

        case 'ON_ERROR':
            return {...action.error};

        default:
            return state;
    }
}

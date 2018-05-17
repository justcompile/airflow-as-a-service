const initialState = null;


export default function dbTypes(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_DB_TYPES':
            return [ ...action.dbTypes ];

        default:
            return state;
    }
}

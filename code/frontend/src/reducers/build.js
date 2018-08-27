const initialState = null;


export default function build(state=initialState, action) {
    switch (action.type) {

        case 'GET_BUILD':
            return { ...action.build };

        default:
            return state;
    }
}

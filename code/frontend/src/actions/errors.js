export const clear = () => {
    return dispatch => {
        return dispatch({
            type: 'CLEAR_ERRORS',
        });
    }
}

export const errorHandler = (dispatchFunc, e) => {
    return dispatchFunc({
        type: 'HTTP/REQUEST/ERROR',
        error: e
    })
};
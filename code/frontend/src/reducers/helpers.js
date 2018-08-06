export const updateStateFromSocket = (key, orginalState, action) => {
    if (action.payload.id === key) {
        const newEntity = JSON.parse(action.payload.event.data);
        const idx = orginalState.findIndex(element => element.id === newEntity.id);
        if (idx >= 0) {
            const clone = [...orginalState];
        
            clone[idx] = newEntity;
            return clone;
        }
    }

    return orginalState;
};
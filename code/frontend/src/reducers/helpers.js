export const updateStateFromSocket = (key, originalState, action) => {
    if (action.payload.id === key) {
        const message = JSON.parse(action.payload.event.data);

        const desiredAction = message.action;
        const entity = message.data;

        console.log(entity);
        switch (desiredAction) {
            case 'UPDATE':
                const idx = originalState.findIndex(element => element.id === entity.id);
                if (idx >= 0) {
                    const clone = [...originalState];
                
                    clone[idx] = entity;
                    return clone;
                }
            case 'CREATE':
                return [entity, ...originalState];
            default:
                return originalState;
        }        
    }

    return originalState;
};
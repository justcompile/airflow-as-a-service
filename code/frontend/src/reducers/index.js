import { combineReducers } from 'redux';
import repos from "./repos";
import clusters from "./clusters";
import cluster from "./cluster";
import clusterEvents from "./clusterEvents";
import dbTypes from "./dbTypes";


const airflowAsAServiceApp = combineReducers({
    repos,
    clusters,
    cluster,
    clusterEvents,
    dbTypes,
})

export default airflowAsAServiceApp;

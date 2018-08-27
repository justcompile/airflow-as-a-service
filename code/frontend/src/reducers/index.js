import { combineReducers } from 'redux';
import repos from "./repos";
import github from "./github";
import clusters from "./clusters";
import cluster from "./cluster";
import clusterEvents from "./clusterEvents";
import dbTypes from "./dbTypes";
import payments from "./payments";
import plans from "./plans";
import build from "./build";
import builds from "./builds";
import logs from "./logs";
import errors from "./errors";

const airflowAsAServiceApp = combineReducers({
    clusters,
    cluster,
    clusterEvents,
    dbTypes,
    github,
    repos,
    payments,
    plans,
    builds,
    build,
    errors,
    logs,
})

export default airflowAsAServiceApp;

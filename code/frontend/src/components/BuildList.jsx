import React, { Component } from 'react';
import {connect} from 'react-redux';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

import BuildListItem from './BuildListItem';
import {builds} from "../actions";


class BuildList extends Component {
    componentDidMount() {
        this.props.fetchBuilds();
        this.props.listenForBuilds();
    }

    componentWillUnmount() {
        this.props.disconnect();
    }

    render() {
        return (
            <div>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">Builds</Typography>
                    </Grid>
                </Grid>
                <div>
                    {this.props.builds.map((build, id) => (
                    <BuildListItem build={build} key={`build_${build.id}`} />
                ))}
                </div>
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        builds: state.builds,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchBuilds: () => {
            dispatch(builds.fetchBuilds());
        },
        updateBuildStatus: (build) => {
            dispatch(builds.updateBuildStatus(build));
        },
        listenForBuilds: () => {
            dispatch(builds.connectToSocket());
        },
        disconnect: () => {
            dispatch(builds.disconnect());
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(BuildList);


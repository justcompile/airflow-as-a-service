import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import BuildListItem from './BuildListItem';
import BuildLog from './BuildLog';

import {builds} from "../actions";


const styles = _ => ({});

class BuildDetail extends Component {
    componentDidMount() {
        this.props.getBuild(this.props.match.params.buildId);
        this.props.listenForBuilds();
    }

    componentWillUnmount() {
        this.props.disconnect();
    }

    render() {
        const { build } = this.props;

        if (build == null) {
            return (<div></div>);
        }

        return (
            <div>
                <BuildListItem build={build} disableButton={true} />
                <BuildLog buildId={build.id} />
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        build: state.build,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        getBuild: (buildId) => {
            dispatch(builds.getBuild(buildId));
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

BuildDetail.propTypes = {
    classes: PropTypes.object.isRequired,
    match: PropTypes.object.isRequired,
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(BuildDetail));


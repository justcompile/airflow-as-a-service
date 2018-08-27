import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import SyntaxHighlighter, { registerLanguage } from "react-syntax-highlighter/light";
import bash from 'react-syntax-highlighter/languages/hljs/bash';
import tomorrowNight from 'react-syntax-highlighter/styles/hljs/tomorrow-night'; 

import {logs} from "../actions";

registerLanguage('bash', bash);

const styles = _ => ({});

class BuildLog extends Component {
    componentDidMount() {
        this.props.getBuildLog(this.props.buildId);
        this.props.listenForLogs(this.props.buildId);
    }

    componentWillUnmount() {
        this.props.disconnect(this.props.buildId);
    }

    render() {
        const { logs } = this.props;

        if (logs == null || logs.lines === undefined) {
            return (<div>No Log</div>);
        }

        const lines = logs.lines.join('\n');

        return (
            <div>
                <SyntaxHighlighter language='bash' style={tomorrowNight}>{lines}</SyntaxHighlighter>
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        logs: state.logs,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        getBuildLog: (buildId) => {
            dispatch(logs.getBuildLog(buildId));
        },
        listenForLogs: (buildId) => {
            dispatch(logs.connectToSocket(buildId));
        },
        disconnect: (buildId) => {
            dispatch(logs.disconnect(buildId));
        }
    }
}

BuildLog.propTypes = {
    classes: PropTypes.object.isRequired,
    buildId: PropTypes.string.isRequired,
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(BuildLog));


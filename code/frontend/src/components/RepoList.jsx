import React, { Component } from 'react';
import {connect} from 'react-redux';

import {repos} from "../actions";



class RepoList extends Component {

    componentDidMount() {
        this.props.fetchRepos();
    }

    state = {
        text: "",
        updateNoteId: null,
    }

    render() {
        return (
            <div>
                <h3>Repos</h3>
                <table>
                    <tbody>
                        {this.props.repos.map((note, id) => (
                            <tr key={`note_${note.url}`}>
                                <td>{note.name}</td>
                                <td><a href={`${note.url}`} target="_blank">view</a></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        repos: state.repos,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchRepos: () => {
            dispatch(repos.fetchRepos());
        },
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(RepoList);

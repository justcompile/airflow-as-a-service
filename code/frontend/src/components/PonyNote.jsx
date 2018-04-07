import React, { Component } from 'react';
import {connect} from 'react-redux';

import {notes} from "../actions";



class PonyNote extends Component {

    componentDidMount() {
        this.props.fetchNotes();
    }

    state = {
        text: "",
        updateNoteId: null,
    }

    resetForm = () => {
        this.setState({text: "", updateNoteId: null});
    }

    nav = (url) => {
        window.location.href = url;
    }

    render() {
        return (
            <div>
                <h3>Repos</h3>
                <table>
                    <tbody>
                        {this.props.notes.map((note, id) => (
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
        notes: state.notes,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchNotes: () => {
            dispatch(notes.fetchNotes());
        },
        addNote: (text) => {
            return dispatch(notes.addNote(text));
        },
        updateNote: (id, text) => {
            return dispatch(notes.updateNote(id, text));
        },
        deleteNote: (id) => {
            dispatch(notes.deleteNote(id));
        },
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(PonyNote);

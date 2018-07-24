import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
// import Input, { InputLabel } from '@material-ui/core/Input';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
// import { FormControl } from '@material-ui/core/Form';
//import Select from '@material-ui/core/Select';

import {connect} from 'react-redux';
import {clusters, repos} from "../../actions";

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 240,
  },
  menu: {
    width: 250,
  },
});

class CreateClusterDialog extends React.Component {
  state = {
    open: false,
    submitted: false,
    dbType: '',
    repository: ''
  };

  componentDidMount() {
    this.props.fetchDBTypes();
    this.props.fetchRepos();
  }

  handleChange = name => event => {
    this.setState({ [name]: event.target.value });
  };

  handleSubmit = () => {
    this.setState({'submitted': true})
    if (this.state.dbType !== '' && this.state.repository !== '') {
      this.props.onSubmit({
        dbType: this.state.dbType,
        repository: this.state.repository
      });
    }
  };

  render() {
    const { classes, open } = this.props;

    if (this.props.dbTypes == null || this.props.repos == null) {
        return null;
    }

    return (
      <div>
        <Dialog
          disableBackdropClick
          disableEscapeKeyDown
          open={open}
          onClose={this.handleClose}
        >
          <DialogTitle>Create Cluster</DialogTitle>
          <DialogContent>
            <form className={classes.container}>
            {this.state.error ? (
              <p>{this.state.error}</p>
            ) : ('')}
              <div className={classes.formControl}>
                <TextField
                  id="db-simple"
                  select
                  className={classes.textField}
                  label="Airflow MetaDB Type"
                  error={this.state.submitted && this.state.dbType === ''}
                  value={this.state.dbType}
                  onChange={this.handleChange('dbType')}
                  SelectProps={{
                    MenuProps: {
                      className: classes.menu,
                    },
                  }}
                >
                  {this.props.dbTypes.map((dbType, id) => (
                    <MenuItem key={id} value={dbType.id}>{dbType.varient} {dbType.version}</MenuItem>
                  ))}
                </TextField>
              </div>
              <div className={classes.formControl}>
                <TextField
                  id="repo-simple"
                  select
                  className={classes.textField}
                  label="Repository"
                  error={this.state.submitted && this.state.repository === ''}
                  value={this.state.repository}
                  onChange={this.handleChange('repository')}
                  SelectProps={{
                    MenuProps: {
                      className: classes.menu,
                    },
                  }}
                >
                  {this.props.repos.map((repo, id) => (
                    <MenuItem key={id} value={repo.id}>{repo.name}</MenuItem>
                  ))}
                </TextField>
              </div>
            </form>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.onCancel} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSubmit} color="primary">
              Ok
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

const mapStateToProps = state => {
    return {
        dbTypes: state.dbTypes,
        repos: state.repos,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchDBTypes: () => {
            dispatch(clusters.fetchDBTypes());
        },
        fetchRepos: () => {
          dispatch(repos.fetchUserRepos());
        }
    }
}

CreateClusterDialog.propTypes = {
  classes: PropTypes.object.isRequired,
  open: PropTypes.bool.isRequired,
  onCancel: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(CreateClusterDialog));
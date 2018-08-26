import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';

import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';


const styles = theme => ({
    button: {
        margin: theme.spacing.unit,
    },
    rightIcon: {
        marginLeft: theme.spacing.unit,
    },
  });

const options = {
    'stopped': ['Start Build'],
    'queued': ['Start Build'],
    'running': ['Stop Build'],
    'failed': ['Restart Build'],
    'success': ['Restart Build'],
};
  
const ITEM_HEIGHT = 48;

class ButtonMenu extends Component {
    state = {
        anchorEl: null,
    };
    
    openMenu = event => {
        this.setState({ anchorEl: event.currentTarget });
    };

    handleClose = (option) => {
        this.props.onSelect(option);
        this.setState({ anchorEl: null });
    };

    render() {
        const { anchorEl } = this.state;
        const { currentStatus, classes } = this.props;

        const open = Boolean(anchorEl);

        const menuIcon = this.state.open ? 
            <ExpandLessIcon className={classes.rightIcon} /> :
            <ExpandMoreIcon className={classes.rightIcon} />;

        return (
            <div>
                <Button variant="contained" color="default" className={classes.button} onClick={this.openMenu}>
                    {currentStatus.toUpperCase()}
                    {menuIcon}
                </Button>
                <Menu
                    id="long-menu"
                    anchorEl={anchorEl}
                    open={open}
                    onClose={this.handleClose}
                    PaperProps={{
                        style: {
                        maxHeight: ITEM_HEIGHT * 4.5,
                        width: 200,
                        },
                    }}
                    >
                    {options[currentStatus].map(option => (
                        <MenuItem key={option} onClick={() => this.handleClose(option)}>
                        {option}
                        </MenuItem>
                    ))}
                    </Menu>
            </div>
        )
    }
}


ButtonMenu.propTypes = {
    classes: PropTypes.object.isRequired,
    currentStatus: PropTypes.string.isRequired,
    onSelect: PropTypes.func.isRequired
};


export default withStyles(styles)(ButtonMenu);

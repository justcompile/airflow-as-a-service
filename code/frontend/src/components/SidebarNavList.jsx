// This file is shared across the demos.

import React from 'react';
import { Link } from 'react-router-dom';
//import { withRouter } from "react-router-dom";

import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import DraftsIcon from '@material-ui/icons/Drafts';
import CodeIcon from '@material-ui/icons/Code';
import DnsIcon from '@material-ui/icons/Dns';
import PaymentIcon from '@material-ui/icons/Payment';
import SendIcon from '@material-ui/icons/Send';

class SidebarNavList extends React.Component {
   render() {
     return (
      <div>
        <ListItem button component={Link} to="/">
          <ListItemIcon>
            <DnsIcon />
          </ListItemIcon>
          <ListItemText primary="Clusters" />
        </ListItem>
        <ListItem button component={Link} to="/repos">
          <ListItemIcon>
            <CodeIcon />
          </ListItemIcon>
          <ListItemText primary="Repos" />
        </ListItem>
        <ListItem button component={Link} to="/plans">
          <ListItemIcon>
            <PaymentIcon />
          </ListItemIcon>
          <ListItemText primary="Plans" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <SendIcon />
          </ListItemIcon>
          <ListItemText primary="Send mail" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <DraftsIcon />
          </ListItemIcon>
          <ListItemText primary="Drafts" />
        </ListItem>
      </div>
     )
    }
}

export default SidebarNavList;
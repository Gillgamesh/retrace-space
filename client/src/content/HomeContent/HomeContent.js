import React, { Component } from 'react';

import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';

import { Link } from 'react-router-dom';

import { withStyles } from '@material-ui/core/styles';

import {
    Chart,
    PieSeries,
    Title
} from '@devexpress/dx-react-chart-material-ui';

import Fab from '@material-ui/core/Fab';

import CodeIcon from '@material-ui/icons/Code';
import HomeIcon from '@material-ui/icons/Home';

import GitHubCircleIcon from 'mdi-material-ui/GithubCircle';

import EmptyState from '../../layout/EmptyState/EmptyState';

const styles = (theme) => ({
  Chart: {
    marginTop: theme.spacing(12)
  },

  button: {
    marginTop: theme.spacing(1)
  },

  buttonIcon: {
    marginRight: theme.spacing(1)
  }
});

class HomeContent extends Component {
  render() {
    // Styling

    const { classes } = this.props;

    var data = [
        {expression: 'Sorrow', val: 0.5},
        {expression: 'Joy', val: 0.5},
        {expression: 'Anger', val: 0.5},
        {expression: 'Surprise', val: 0.5},
    ]
    // Properties
    const { isSignedIn, title } = this.props;

    if (isSignedIn) {
        return (
            <Paper>
                <Chart
                    data={data}
                >
                    <PieSeries
                        valueField="val"
                        argumentField="expression"
                        innerRadius={0.6}
                    />
                    <Title
                        text="Bruh"
                    />
                </Chart>
            </Paper>
        )
      // return (
      //   <EmptyState
      //     icon={<HomeIcon className={classes.emptyStateIcon} color="action" />}
      //     title="No Data Available"
      //     description="Sorry!"
      //   />
      // );
    }

    return (
      <EmptyState
        icon={<CodeIcon className={classes.emptyStateIcon} color="action" />}
        title={title}
        description="The three musketeers, all in one pack in the form of a boilerplate app"
        button={
          <Fab className={classes.button} color="secondary" href="https://github.com/Phoqe/react-material-ui-firebase" rel="noopener noreferrer" target="_blank" variant="extended">
            <GitHubCircleIcon className={classes.buttonIcon} />
            GitHub
          </Fab>
        }
      />
    );
  }
}

HomeContent.propTypes = {
  classes: PropTypes.object.isRequired,

  isSignedIn: PropTypes.bool.isRequired,
  title: PropTypes.string.isRequired
};

export default withStyles(styles)(HomeContent);

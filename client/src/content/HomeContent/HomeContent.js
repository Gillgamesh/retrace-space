import React, { Component } from 'react';

import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';

import {default as data} from '../../data.json'

import { Link } from 'react-router-dom';

import { withStyles } from '@material-ui/core/styles';

import {
    Chart,
    PieSeries,
    Title,
    Legend
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

    // var data = [
    //     {expression: 'Sorrow', val: 0.5},
    //     {expression: 'Joy', val: 0.5},
    //     {expression: 'Anger', val: 0.5},
    //     {expression: 'Surprise', val: 0.5},
    // ]
    // Properties
    console.log(data);
    const { isSignedIn, title } = this.props;
      var dataList = data.map(x => x["expression"]);
      var frequency = {"Sorrow": 0, "Joy": 0, "Anger": 0, "Surprise": 0};
      dataList.forEach(row => {
          frequency[row['emotion']] += 1;
      });
      console.log("frequency");
      var frequencyList = (Object.keys(frequency)).map(
          e => {return {'emotion': e, 'val': frequency[e]}
          });
    if (isSignedIn) {
        return (
            <Paper>
                <Chart
                    data={frequencyList}
                >
                    <PieSeries
                        valueField={"val"}
                        argumentField="emotion"
                        innerRadius={0.6}
                    />
                    <Legend/>
                    <Title
                        text="Reaction Breakdown"
                    />
                </Chart>
                <h1>Most Emotional Phrase:</h1>
                <div>{dataList[0]["message1" || null]}</div>
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
        description="You must be signed in to view your statistics!"
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

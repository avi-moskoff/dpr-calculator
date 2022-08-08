# dpr-calculator

A python file that calculates DPR when run at an event with no TBA support.

DPR is calculated using almost the same system as [OPR](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/), except that we want to find each team's defensive contribution rather than its offensive contribution.

So, we just use the opponent's score rather than a team's score. A DPR of ten means that we can expect the robot to contribute to 10 of their opponent's points. Low DPRs are generally better, as it would mean that the team allowed fewer points from their opponents. One of its biggest limitations is that a competition like ARL may not provide enough matches per team for the algorithm to stabilize, but it should at least give us a good starting point when deciding whether a kitbot is better than the null team.

This project assumes python 3 and numpy as dependencies.

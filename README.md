# Pomodoro Tracker

Many people use Pomodoro technique to study, which consists of 2 stages: *focus* and *rest*. The standard technique uses a combination of 25 minutes
of focus followed by 5 minutes of rest. This doesn't mean that it's mandatory, I, for example, use 50 minutes of focus followed by 10 minutes of rest.
This project tracks all your pomodoro sessions, you just need to input them and the data will be stored.

### Structure of Data

The data have the following columns:

| Column | Description | Type | Example |
| -----: | :---------- |:----:| :------ |
| Date | today's date | string | 2021-04-04 |
| Begin | the start time | string | 13:42 |
| End | the end time | string | 09:56 |
| Platform | the platform that you're studying (A more general category) | string | Coursera |
| Subject | the subject you studied (or the name of the course, for example) | string | Neural Networks and Deep Learning |
| Section | the section/chapter of the material | string | Week 1 |
| Total | the total time of the pomodoro, in minutes | integer | 50 |

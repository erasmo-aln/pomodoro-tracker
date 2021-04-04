# Pomodoro Tracker

Many people use Pomodoro technique to study, which consists of 2 stages: *focus* and *rest*. The standard technique uses a combination of 25 minutes
of focus followed by 5 minutes of rest. This doesn't mean that it's mandatory, I, for example, use 50 minutes of focus followed by 10 minutes of rest.
This project tracks all your pomodoro sessions, you just need to input them and the data will be stored.

### Structure of Data
The data have the following columns:

- **Date**: today's date (it's automatically inserted). Format: ***2021-04-04***
- **Begin**: the start time. Format: *13:24*. ***Remember to use 24-hour format.***
- **End**: the end time. Format: *14:14*. ***Remember to use 24-hour format.***
- **Platform**: the platform that you're studying (name of the website, book, etc. A more general category). Format: ***string***
- **Subject**: the subject you studied, for example, probability, calculus, python, etc. Format: ***string***.
- **Section**: the section of the material, for example, chapter 3, lecture 5, video 21, etc. Format: ***string***
- **Total**: the total time of the pomodoro, in minutes. Format: ***integer***, for example: 50.

### How to Use
You just need to clone the repository and run the ***app.py*** file and input the data. Also, you'll need the Pandas package.

***Obs:*** If you wrongly filled data to it, you can open the *data/dataset.csv* file and erase/edit the wrong record.

For now, it is a very simple tool but I implemented it to help me track my study hours, that way I can analyze later to see how many hours
of effort was dedicated to each course, chapter and subject. With time, I'll continue to improve this tool to give some analytics and improve
the data input method.

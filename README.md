[![Build Status](https://travis-ci.org/rtfoley/scorepy.svg?branch=master)](https://travis-ci.org/rtfoley/scorepy) [![Stories in Ready](https://badge.waffle.io/rtfoley/scorepy.png?label=ready&title=Ready)](https://waffle.io/rtfoley/scorepy)
# ScorePy
An attempt at an FLL tournament scoring application using Python and Flask

### Main features
- Add/ edit/ remove teams, robot game scores, judge evaluations, and award winners
- Import CSV team list
- Generate team list, robot score rankings, award winner, and category result reports
- Real-time rankings display
- User system for basic security
- Manage playoff rounds and scores

### Installing and running the application on Windows
1. Download the latest release from the [releases](https://github.com/rtfoley/scorepy/releases) page
2. Run the msi installer
3. Double-click the shortcut on the desktop, which should open a command window and start the webserver.
4. Navigate to http://localhost:8080/
5. Login with username 'admin' and password 'changeme'
6. Change the password.

### Installing and running the application on MacOS
Coming soon...



### Setting up for development
Install Python 2.7.x: https://www.python.org/downloads/

Install pip: https://pip.pypa.io/en/latest/installing.html

Install virtualenv
```text
> pip install virtualenv
```

Clone the repository
```text
> git clone https://github.com/rtfoley/scorepy.git
```

Create a virtual environment
```text
> cd scorepy
> virtualenv venv
```
Activate the virtual environment using one of the following commands:

Windows systems:
```text
> .\\venv\Scripts\activate
```

Unix systems:
```text
> source venv/bin/activate
```

Use Pip to install dependencies
```text
(venv) > pip install -r requirements.txt
```

Run the application
```text
(venv) > python run.py
```

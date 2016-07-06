[![Stories in Ready](https://badge.waffle.io/rtfoley/scorepy.png?label=ready&title=Ready)](https://waffle.io/rtfoley/scorepy)
# ScorePy
An attempt at an FLL tournament scoring application using Python and Flask

### Existing Functionality
- Add/ edit/ remove teams, robot game scores, judge evaluations, and award winners
- Import CSV team list
- Generate team list, robot score rankings, award winner, and category result reports
- Real-time rankings display
- User system for basic security
- Manage playoff rounds and scores

### Planned future functionality
- [ ] import a match schedule
- [ ] announcers report
- [ ] event settings page (event name)
- [ ] playoff display

### Possible future features
- [ ] state championship qualifying report
- [ ] automatic award winner selection
- [ ] referee interface
- [ ] head referee interface

### Setting up and running the application:
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
> cd fllipit
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

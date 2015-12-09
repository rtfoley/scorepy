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

### Future functionality
- [ ] import a match schedule
- [ ] announcers report
- [ ] event settings page (event name)
- [ ] automatic award winner selection
- [ ] state championship qualifying report
- [ ] playoff display
- [ ] individualized team results reports
- [ ] save database via UI
- [ ] upload database via UI
- [ ] generate a match schedule
- [ ] referee interface
- [ ] head referee interface
- [ ] judges interface (with ability to add notes)

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

# ScorePy
An attempt at an FLL tournament scoring application using Python and Flask

### 2015 Progress
- [x] basic layout (layout.html, navbar, footer, bootstrap/ fontawesome)
- [x] page shells (main, about, teams, awards, playoffs, pit display, playoff display)
- [ ] event settings page (event name)
- [x] team list page
- [x] team management via form
- [x] team CSV import
- [x] team list report
- [x] basic score management per team (with team and round selection, but using simplified score form)
- [x] full 2015 score form
- [x] rankings report
- [ ] qualification rankings display
- [x] judge evaluation management
- [ ] automatic award winner selection
- [ ] manual award winner selection
- [ ] award winner report

### Future functionality
- [ ] state championship qualifying report
- [ ] login system
- [ ] playoff management
- [ ] playoff display
- [ ] individualized team results reports
- [ ] save database via UI
- [ ] upload database via UI
- [ ] import a match schedule
- [ ] generate a match schedule
- [ ] announcers report
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

# ScorePy
An attempt at an FLL tournament scoring application using Python and Flask

### Progress
- [x] basic layout (layout.html, navbar, footer, bootstrap/ fontawesome)
- [x] page shells (main, about, teams, awards, playoffs, pit display, playoff display)
- [ ] login system
- [ ] event settings page (event name, passwords)
- [x] team list page
- [x] team management via form
- [x] team CSV import
- [x] team list report
- [x] basic score management per team (with team and round selection, but using simplified score form)
- [ ] full 2015 score form
- [x] rankings report
- [ ] qualification rankings display
- [x] judge evaluation management
- [ ] award selection
- [ ] manual award winner selection
- [ ] automatic award winner selection
- [ ] award winner report
- [ ] state championship qualifying report

### Bonus functionality
- [ ] playoff management
- [ ] playoff display
- [ ] save database via webpage
- [ ] upload database via webpage

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

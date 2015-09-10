# ScorePy
An attempt at an FLL tournament scoring application using Python and Flask

### Prototype progress
- [x] Ability to calculate a score live as form is changed
- [x] Ability to save scores to a database
- [x] Ability to edit previously entered scores
- [ ] Ranking report (.pdf)
- [ ] Pit display that shows live-updating rankings
- [ ] Save database via webpage
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
(venv) > python main.py
```

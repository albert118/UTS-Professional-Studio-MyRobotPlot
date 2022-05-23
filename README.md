# My Robot Plot

_UTS Professional / Applications Studio Project_

My Robot Plot is a project designed to gain an improved understanding towards a specific type of machine learning called Natural Learning Processing, designed to predict and estimate word and sentence generation. The basic dataset that will be used by the team will consist of movie plots taken from public data sources, such as Wikipedia. The team aims to generate and develop new movie plots based off existing information, and ultimately create a machine learning model that can create understandable and fluent movie plots. This exercise will allow for a better understanding of the power of NLP and its subcomponents. 

### Environement Set up
Using Python verison 3.9.+ to 3.10.0, set up the environment like so.

Create and source your choice of virtual environment, eg. [venv](https://virtualenv.pypa.io/en/latest/). I also recommend the [win wrapper](https://pypi.org/project/virtualenvwrapper-win/) if you're on Windows. Activate it, then install the dependencies with pip like so,

```
// once in your development environ
pip install -r requirements
```

### Running the Pipeline Project(s)

Run the package as expected with,

```
python -m MyRobotPlot
```

### Runnning the Web App (++ extra)

1. Set the environ' variable for flask, eg.

```
// on Windows
set FLASK_APP=web_app
// on Linux
export FLASK_APP=web_app
```

2. Initialise the database

Run the following to bootstrap the db, then automatically run the initial schema migration. This should create a database.py file.

```
python -m init_database
```

3. In you Python environment, run the following command to execute the Flask server.

```
flask run
```

For more info, see the [Flask QuickStart Guide](https://flask.palletsprojects.com/en/1.1.x/quickstart/).

### Updating the Package Requirements

Install your packages into the virtualenv, ensure they are as you expect with `pip list`. Then, once you're happy execute the following to update the `requirements` file.

```
pip freeze -r > requirements
```

Done!


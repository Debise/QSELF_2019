# QSELF_2019

## Installation

To use our project. One need to use pipenv. 

```
pip install pipenv
```

Once it's installed, run the command `pipenv install` in the root folder. Everything is going to be installed automatically.

Pipenv will create a virtual environnement with all the needed dependances inside for you.

Common pipenv commands :

 * `pipenv shell` : It will put you inside the virtual env shell.
 * `pipenv run your command` : It will run `your command` inside the virtual env without the need to be inside.

## Usage

For the moment, to run the viewer, you need to :

 * First be located on the viewer folder.
 * Then run the command : `pipenv run python run_server.py`
 * You can now access the viewer with the address `127.0.0.1:5000` on your browser.

 To regenerate the *pickle* files (RaceManager & RaceInferer) from the races source file (`.fit`):

 * In `main.py` : Set to `1` the 2 variables `process_all_race` & `infer_all`
 * Run the command : `pipenv run python main.py`
 * This will regenerate the pre-processed data for the viewer 
 * This operation will take about 1h30 to complete

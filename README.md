# Seat Tracker

This project provides a simple RESTful interface that allows modification and tracking of events and seats for those 
events. 

## Deployment

Simply install into a Python-compatible shell. We recommend using the Python installer `pip` to install the following 
required packages:

* pip - see instructions at https://pip.pypa.io/en/stable/installing/
* virtualenvwrapper - see instructions at https://virtualenvwrapper.readthedocs.io/en/latest/

After creating an environment for this package (e.g. `seats`), you can complete installation by installing the required 
Python packages:

```bash
workon seats
pip install -r requirements.txt
```

## Execution

The server is run by executing the main python code in seats.py:

```bash
$ python seats.py
 * Serving Flask app "seats" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 291-107-388
```

## API

The following routes are available:

| HTTP Method | URI     | Action                                                              |
| ----------- | ------- | ------------------------------------------------------------------- |
| GET         | `/events` | List all event ids (or complete details if 'verbose' is True).      |
| GET         | `/events/<id>` | Get full details for an event. |
| GET         | `/events/<id>/seats` | Get seat details. |
| POST        | `/events` | Create an event (automatically assigns the next id (starting at 1). |
| POST        | `/events/<id>/seats/<id>` | Create a seat for the given event. |

#### POST `/events`

If the parameter `verbose` is specified and set to `True` the entire event details are returned. Otherwise, only
a list of event ids is returned.

#### POST `/events/<id>/seats/<id>`
 
Supports the following optional arguments. If a value is not specified, the corresponding default is used:

| argument | default |
| -------- | ------- |
| type | 'adult' |
| aisle | False |
| available | True |


## Testing

Integration tests can be run against a fresh running copy of `seats.py` using `nosetests`:

```bash
$ nosetests

----------------------------------------------------------------------
Ran 3 tests in 0.333s

OK
```

See test.py for full test details.

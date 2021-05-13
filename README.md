# TigerCard POC application

## Setup

Clone the repository from:

```sh
$ git clone https://github.com/rahulagarwal86/tigercard-poc.git
$ cd sample-django-app
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --python=python3.7 venv
$ source env/bin/activate
```

Install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd tigercard
(env)$ python manage.py runserver
```
In order to calculate the fare for an individual, use any rest client. Below is the API request detail:

### Request

`POST /api/v1/calculate-fare/`

    curl -i -H 'Accept: application/json' -d 'journey_list=[{"date-time": "2020-01-01 09:00:00", "from_zone": 3, "to_zone":2},]' http://localhost:8000/api/v1/calculate-fare/

### Response

    HTTP/1.1 200 Created
    Date: Thu, 24 Feb 2021 12:36:31 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {'total_fare': 30}

##API Payload
`Method: POST`

`URL: /api/v1/calculate-fare/`

`REQUEST PARAMS`
     
     <List of dictionary containing detail of each journey>
     
     Dictionary Params:
     
     "date-time: <Datetime string in format YYYY-MM-DD HH:MM:SS>" 
     "from_zone": <int>
     "to_zone": <int>
 
 `RESPONSE DATA`
 
     "total_fare": <int>
     
## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(venv)$ python manage.py test
```

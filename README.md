# xtrade

webapp to Trade on Binance.
It uses Binance API to send/cancel orders.

## Setup steps:

create a virtual env with python3:

```commandline
python3 -m pip install venv
python3 -m venv venv310
```

Use virtual env:

```commandline
source venv310/bin/activate
```

Clone the repo:
```commandline
git clone https://github.com/itzmestar/xtrade
```

Install requirements:
```commandline
cd xtrade
python3 -m pip install -r requirements.txt
```

Create DB:
```commandline
python3 manage.py makemigrations
python3 manage.py migrate
```

Create a superuser:
```commandline
python3 manage.py createsuperuser
```

## To Run local server:
```commandline
python3 manage.py runserver
```

this will run the webapp on localhost on port 8000

Access the GUI here: http://127.0.0.1:8000/

Login with superuser credentials

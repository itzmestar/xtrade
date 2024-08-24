# xtrade

webapp to Trade on Binance.
It uses Binance API to send/cancel orders.

Trade history can also be viewed which is not available on Binance App.

## Setup steps:

create a virtual env with python3:

```commandline
python -m pip install venv
python -m venv venv310
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
python -m pip install -r requirements.txt
```

Create DB:
```commandline
python manage.py makemigrations
python manage.py migrate
```

Create a superuser:
```commandline
python manage.py createsuperuser
```

## To Run local server:
```commandline
python manage.py runserver
```

this will run the webapp on localhost on port 8000

Access the GUI here: http://127.0.0.1:8000/

Login with superuser credentials

# reddit-clone

A very simple clone of Reddit

## Setup

To develop locally, do following steps:

- Clone the repository and cd to it

```
git clone https://github.com/shivams906/reddit-clone.git
cd reddit-clone
```

- Create a virtual environment and activate it

```
python -m venv venv
source venv/bin/activate
```

- Install the requirements

```
pip install -r requirements.txt
```

- Set up the database

```
python manage.py migrate
```

- Run the server

```
python manage.py runserver
```

## Tests

Run the following command

```
python manage.py test --settings config.settings_for_tests
```

## Coverage

Run

```
coverage run --source='.' manage.py test --settings config.settings_for_tests
```

- For report in terminal

```
coverage report
```

- For html report, run the following command and open the file htmlcov/index.html in your browser

```
coverage html
```

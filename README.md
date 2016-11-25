# test_rent
[![PyPI](https://img.shields.io/pypi/pyversions/superset.svg?maxAge=2592000)](https://pypi.python.org/)
[![Build Status](https://travis-ci.org/airbnb/superset.svg?branch=master)]


# Rent-o-Matic

Demo projec that allows us to rent transport, payment is in cash and calculate the change in the lower quantity of paper money to give

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
```
git clone https://github.com/walterpk78/test_rent
```
### Prerequisites

Django-1.10.3, python-2.7.5, django-tables2, psycopg2, selenium(optiona for testing frontend), unittest(optional testing backend)

```
Django==1.10.3
django-tables2==1.2.6
pkg-resources==0.0.0
psycopg2==2.6.2
```

### Installing
Installing a virtualenv (optional)
```
virtualenv virtalenv/renting
```
Installing packages from requirements.txt
```
pip install -r requirements.txt 
```

Database preparation(mandatory):
open settings.py set your database credentials and then create database
```
postgres=#  create role rent;
postgres=#  create database rent owner by rent;
postgres=#  \c rent
rent=# create schema rent;
```
give permissions with GRANT as your desire

example database insertion of different renting transports
```
insert into rentomatic_transport (id, transport_type, description, price_per_day, km, rented, rented_until ) VALUES (3,2,'Luxury car, very confortable, nice looking', 10000, 1500, False, NULL);
insert into rentomatic_transport (id, transport_type, description, price_per_day, km, rented, rented_until ) VALUES (2,2,'Good family car, nice condition, ready to discover new places', 100, 150, False, NULL);
insert into rentomatic_transport (id, transport_type, description, price_per_day, km, rented, rented_until ) VALUES (1,1,'Best bike ever, good breakes, not heavy and good red color', 100, 150, False, NULL);
```
run django migrations
```
cd renting
python manage.py migrate
python manage.py makemigrations
```
Logs files: we recommend creating separated logs as example in settings.py, but in the demo we use api.log
```
touch LOGS/api.log

```
## Running system
open a web browser and point it to your port(optional for tensting)
```
# manage.py runserver localhost:8080
```

## Deployment

This is a normal django app you can use any deployment system like Jenkins

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Walter Kuhn** - *Initial work* - [PurpleBooth](https://github.com/walterpk78)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc


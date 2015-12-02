# The BucketList App [![Build Status](https://travis-ci.org/andela-uawili/django-bucketlist-application.svg?branch=develop)](https://travis-ci.org/andela-uawili/django-bucketlist-application) [![Coverage Status](https://coveralls.io/repos/andela-uawili/django-bucketlist-application/badge.svg?branch=develop&service=github)](https://coveralls.io/github/andela-uawili/django-bucketlist-application?branch=develop)

A simple, easy to use app that helps you organize and manage collections of bucket lists. Bucket lists are a cool way to keep track of all the oh-so-great-and-mighty things you plan do before you...erm...erm. 

## Features
+ A simple and responsive web app. You can try it out [here](http://thebucketlistapp.herokuapp.com/).
+ RESTful, well documented API. See the API documentation [here](http://thebucketlistapp.herokuapp.com/api/docs/).

## Tech
Some of the open projects leveraged in building The BucketList App include:
+ [Django](https://www.djangoproject.com/) - Python web development framework for building web apps quickly and with less code.
+ [Django REST Framework](http://www.django-rest-framework.org/) - powerful and flexible toolkit for building Web APIs in Django.
+ [PostgreSQL](http://www.postgresql.org/) - relational database management system.
+ [Swagger UI](http://swagger.io/) - tool for interactive documentation of RESTful APIs
+ [Bower](http://bower.io/) - front end javascript dependency manager.
+ [MaterializeCSS](http://materializecss.com/) - modern responsive front-end framework based on Material Design.
+ [jQuery](http://jquery.com/) - fast, small, and feature-rich JavaScript library.
+ [Packery](http://packery.metafizzy.co/) - a clever grid and bin-packing layout library.
+ [Flickity](http://flickity.metafizzy.co/) - a front-end library for responsive, flickable galleries.

## Usage

#### Installation
Follow the steps below to install The BucketList App on your local machine: 

1. Ensure you have Python >= 2.7 installed. You can get it [here](https://www.python.org/downloads/). Using a virtual environment is also recommended.
2. Ensure you have **npm** and **bower** installed. You can get **npm** [here](https://www.npmjs.com/).
3. Ensure you have PostgreSQL installed and create a database with the name `bucketlist`.
4. Clone this repository to your machine.
5. In the project root, add a `.env.yml` file to hold all your environment variables, such your secret key (required) and database credentials e.g:
    ```
    SECRET_KEY:
    'very-very-very-secret-key'
    DATABASE_USER:
    'foo_user'
    DATABASE_PASSWORD:
    'youcannotguessme' 
    ```

6. Install all python and front end dependencies by running the followings commands in order, from in the project root:
    ```
    $ npm install -g bower
    $ bower install
    $ pip install -r requirements.txt
    ```

7. To setup static files and database migrations, run (also in the project root):
    ```
    $ bucketlist/python manage.py collectstatic
    $ python bucketlist/manage.py makemigrations
    $ python bucketlist/manage.py migrate
    ```
 
#### Running the Server

Run `$ bucketlist/python manage.py runserver` to start the server.

#### Testing
+ To run tests:  
```$ python bucketlist/manage.py test --settings=bucketlist.settings.testing```

+ For the coverage report:    
  1. ```$ coverage run --source=dasboard,api bucketlist/manage.py test bucketlist --settings=bucketlist.settings.testing ```
  2. ```$ coverage report ```
  3. ```$ coverage html ```

## Mockups:
Some of the high-fidelity mockups created for the UI have been included in this repo in the `/mockups` folder.
+ [Landing View](https://github.com/andela-uawili/django-bucketlist-application/blob/develop/mockups/Landing.png")
+ [Dashboard View](https://github.com/andela-uawili/django-bucketlist-application/blob/develop/mockups/dashboard.png")

## Licence:
GNU GPL

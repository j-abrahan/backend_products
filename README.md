# Django REST API backend encapsulated using Docker and docker-compose

### Description
Django REST API backend. Allows customers to order products.

### Setup the application:
The app is packed using Docker and Docker Compose. Follow the instructions below to install both:
- Setup [Docker](https://docs.docker.com/install/)
- Setup [Docker Compose](https://docs.docker.com/compose/install/)
- Next, clone this project.

``` bash
$ git clone https://github.com/j-abrahan/backend_products.git
```

- Build and run application using docker-compose. First time it will take some minutes to install all required packages.

``` bash
$ docker-compose up -d --build
```

- Database migrations are run before starting the Django server
- The application will run by default on localhost IP 0.0.0.0:8000, therefore point navigator to address http://0.0.0.0:8000/products

### Running the tests
The tests are implemented using pytest and pytest-django. See requirements.txt

The Django tests create their own throaway DB, therefore they can be run at the same time that the application is running without
affecting the application DB.
IMPORTANT NOTE: The tests rely on the initially provided migration data products/migrations/

``` bash
docker-compose exec products pytest -v
```

### Stopping the app

``` bash
$ docker-compose down
```

# Restart the app (Migrations will be run again)

```
$ docker-compose up -d --build
```

### BASIC DEBUGGING

- See running containers created by docker-compose
``` bash
$ docker ps
```

- See container logs

``` bash
$ docker-compose logs -f
```

- Open a shell to the running container

``` bash
$ docker-compose exec products bash
```

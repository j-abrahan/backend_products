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
- The application will run by default on localhost IP 0.0.0.0:8000, therefore point navigator to address http://0.0.0.0:8000 or http://0.0.0.0:8000/products

### Create superuser (For the coming examples username:root - password:root are assumed)
``` bash
$ docker-compose exec products ./manage.py createsuperuser
```

### Endpoint Examples
All the following pictures were taken from the Command line output from httpie. These examples may not reflect the migrations initial data and
are presented just as a demo.

### Registering a non admin user
``` bash
http --json POST http://0.0.0.0:8000/register/ username="pepito3" password="xona1234" password2="xona1234"
```

![imagen](https://user-images.githubusercontent.com/96445374/159169617-f2dbe7f3-d98c-4a4d-9466-76e549dca540.png)

### Getting API token for the previous user
``` bash
http --json POST http://0.0.0.0:8000/api-token-auth/ username="pepito3" password="xona1234"
```

![imagen](https://user-images.githubusercontent.com/96445374/159169675-fe4612b8-9015-449e-9c85-07ee76b6a40b.png)

### Getting products list (open to anyone)
``` bash
http --json GET http://0.0.0.0:8000/products/  
```

![imagen](https://user-images.githubusercontent.com/96445374/159169790-06704b45-aedd-4ea6-91b5-0b92ae744c58.png)

### User makes an order (Product name "Lardo")
``` bash
http --json POST http://0.0.0.0:8000/products/orders/ name="Lardo" quantity=3 "Authorization: Token 9a97b3468ee0d38afa63945ef7411cb31f972681"
```

![imagen](https://user-images.githubusercontent.com/96445374/159169898-a9da8914-a1aa-448d-beba-f99b2ae79e6f.png)

### Getting updated "Lardo" product id 7 (previous quantity value from products list picture above 7, new value 4)
``` bash
http --json GET http://0.0.0.0:8000/products/7/
```

![imagen](https://user-images.githubusercontent.com/96445374/159170001-325c7581-1bcb-4a64-89ee-d0ce5d8a70b7.png)

### Getting previous orders (Only orders by the current logged user are shown)
``` bash
http --json GET http://0.0.0.0:8000/products/orders/ "Authorization: Token 9a97b3468ee0d38afa63945ef7411cb31f972681"
```

![imagen](https://user-images.githubusercontent.com/96445374/159170181-4be6e9c8-d3b6-40c4-b65c-6b64f3e56bae.png)

### Adding a product (Using a regular customer/user account it not possible)
``` bash
http --json POST http://0.0.0.0:8000/products/ name="Bananas" price="3" quantity=10 "Authorization: Token 9a97b3468ee0d38afa63945ef7411cb31f972681"
```

![imagen](https://user-images.githubusercontent.com/96445374/159170436-2b0a499b-d052-43cc-830b-deea425f918f.png)

### Adding a product (Using admin user)
``` bash
http --json POST http://0.0.0.0:8000/products/ name="Bananas" price="3" quantity=10 "Authorization: Token $(cat token)"
```

![imagen](https://user-images.githubusercontent.com/96445374/159170530-423671e7-d303-475f-8815-5554642bf38b.png)

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

### Restart the app (Migrations will be run again)

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

### Bonus points

### Deployment instructions for Heroku

1. Install a production server to be used instead of the default Django server. For example, Gunicorn.
2. Update requirements.txt file with Gunicorn related dependencies.
3. Create a runtime.txt file next to requirements.txt to specify the Python version to run on Heroku
4. Update the ALLOWED_HOSTS configuration adding ".herokuapp.com"
5. Create a Procfile for Heroku at the same level as manage.py that tells Heroku that Gunicorn is used as webserver

### Future work

- Extend unit tests.
- Add code coverage reports based on unit tests.
- Implement handling ordering multiple products in the same request.
- Implement product based statistics, for instance, most ordered product, total price paid per product. Both for different
time periods, all time, year to day, last month, last week.
- Add advanced debugging information, how to run a debugger with the Docker running app

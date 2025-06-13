# claims API

## Run
To run the claims API in a docker compose setup follow the steps:
- Step 1. ``docker compose build ``
Execute as root, or with sudo if you get permission errors.

- Step 2. ``docker compose run  evm-api python manage.py runserver ``
Check if everything runs smoothly, and if ok perform stop the containers with Crt-C.
Note that this might give you an error if you have firewall running. Assure that the postgres container can be accessed from the evm-api container.

- Step 3. ``docker compose run  evm-api python manage.py migrate``
Run the migration if there is a warning regarding the missing migrations.
After migration you need to run the server as per step 4.

- Step 4. ``docker compose up``
Run the server mode in production mode.


## To the django project from scratch (not required)

- Step 1. ``docker compose run evm-api django-admin startproject evmAPI . `` 
  This step builds the contains in the `docker-compose.yaml` file, namely the db and the evm-API. 

- Step 2. Edit the file `evmAPI/settings.py` and change the default database to: 
```
'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
```

Additionally, add import the os module at the beggining of the file
```
import os
```

Also add set the connection to ALLOW all the hosts:
```
ALLOWED_HOSTS = ['*']
```

- Step 3. start the Dockers with `docker compose up`

- Step 4. Run the migration if there is a warning regarding the missing migrations. Example of warning: *You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions* :
``docker exec -it claimsdata-evm-api-1 python manage.py migrate``



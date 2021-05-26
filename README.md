# Simple Model Registry

Provides an interface to register model metadata and have a simple lifecycle.

All metadata relies on a Mssql Server instance but could easily be extended with the help of sqlalchemy.

## Startup

Code to start the interface
```
docker run -d -p 80:80 -e DATABASE_HOST=<db-host> -e DATABASE_NAME=<db-name> -e DATABASE_USER=<db-user> -e DATABASE_PASSWD=<db-password> --net local-net --name model-registry-api model_registry_api:0.1
```

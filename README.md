# Service for tracking incoming meetup users

## Installation

* Install [Docker](https://docs.docker.com/engine/install/ubuntu/) and 
[docker-compose](https://docs.docker.com/compose/install/):

* Then you can start the service with the following command:

  ```shell
  DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose --compatibility up --build --force-recreate --detach \
  --scale base=0 --scale app=1
  ```
##### .env - file with environment variables


## Documentation
API documentation [docs](http://localhost:8002/docs)

Additional websocket paths:
* /ws/meetup/{meetup_id}/map - every 10 seconds returns statistics about last arrived user  
  **token:** required query parameter (default=X-Token)

* /ws/meetup/{meetup_id}/boarding - show last arrived user’s statistics in realtime
when check validity API is called. 
  **token:** required query parameter (default=X-Token)


## Testing
For testing purposes there are migrations in **alembic/versions** (release migration directory) and **alembic/unittest**
(unit tests migration directory) with init values for API tests with id's 1 and 2. (id not provided in migrations due 
to issues with sequences) 
  
To run tests execute command inside docker container:
```
pytest
```

# GITHUB API microservice

## Quick intro
to run application you need: 
* **docker**
* **docker-compose**

To start application please checkout the source code and in the directory execute:
 
`docker-compose up -d`

Application should be accessible on `http://127.0.0.1:8081` or to test api `http://127.0.0.1:8081/test`


## Design
![api][images/api_example.png]
Application consist of 6 components
* **PROXY** handles routing between api servers
* **API-A** handles client requests and parse data
* **API-B** *same as API-A*
* **REDIS** store queries for api calls
* **DATABASE** stores all the data
* **CRON** request cache update and requests bootstrap db 

Everything is being run in docker and tied together with docker-compose
> For scheduling I've used simple crontab and api call, better solution would be task scheduler, but due how python works this solution was more straight forward


* **Stack**
Uses docker-compose `.env` for local and environment variables on host

* **Proxy**
  Uses nginx image and nginx configuration

* **API**
Uses python image, application is written with flask framework and being run  inside gunicorn Python WSGI HTTP server

* **REDIS**
Uses redis image

* **DATABASE**
Uses database image, and db is configured using script `init-db.sh`

* **CRON**
Uses centos7 image with running cron

## Running application
Application can be started using `docker-compose up -d`

Application has following api:
* `http://127.0.0.1:8081/api/kubernetes`
* `http://127.0.0.1:8081/api/activity/kubernetes`
* `http://127.0.0.1:8081/api/popularity/kubernetes`

For maintenance
* `http://127.0.0.1:8081/bootstrap_db`
* `http://127.0.0.1:8081//update_cache`

## Testing
To run unit test you will need to install python dependecies using: `pip install -r requirements.txt` afterwards execute `python -m unittest discover -s app/`

Application has performance tests which is written using locust framework to execute performance test please start application using command `locust --host=http://0.0.0.0:8081`, `--host` point to application endpoint, afterwards open `http://127.0.0.1:8089` and specify load.
![api][loucst_test.png]

## Performance
Application can about 150 RPS on 4CPU/8GB, main bottle neck at this point is gunicorn configuration, in current default setup is running on 4 worker threads, if I switched to asnyc gevent, I might improve performance considerably



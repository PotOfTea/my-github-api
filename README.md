# GITHUB API microservice

## Quick intro
to run application you need: 
* **docker**
* **docker-compose**

To start application please checkout the source code and in the directory exectute:
 
`docker-compose up -d`

Application shoule be accesibe on `http://127.0.0.1:8081` or to test api `http://127.0.0.1:8081/test`


## Design
Application consist of 6 components
* **PROXY** handles routing between api servers
* **API-A** handles client requests and parse data
* **API-B** *same as API-A*
* **REDIS** store queries for api calls
* **DATABASE** stores all the data
* **CRON** request cache update and requests boostrap db 

Everyhing is being run in docker and tied toghethere with docker-compose
> For scheduling I've used simple crontab and api call, better solution would be task scheduler, but due how python works this soultion was more stright forward


* **Stack**
Uses docker-compose `.env` for local and enviroment variables on host

* **Proxy**
  Usess nginx image and nginx configuration

* **API**
Uses python image, application is writen with flask framework and being run  inside gunicorn Python WSGI HTTP server

* **REDIS**
Uses redis image

* **DATABASE**
Uses database image, and db is configured using scirpt `init-db.sh`

* **CRON**
Uses centos7 image with running cron

## Running application
Appplication can be started using `docker-compose up -d`

Application has following api:
* `http://127.0.0.1:8081/api/kubernetes`
* `http://127.0.0.1:8081/api/activity/kubernetes`
* `http://127.0.0.1:8081/api/popularity/kubernetes`

For maintance
* `http://127.0.0.1:8081/bootstrap_db`
* `http://127.0.0.1:8081//update_cache`

## Testing
To run unit test you will need to install python dependecies using: `pip install -r requirements.txt` afterwards exectute `python -m unittest discover -s app/`

Application has performance tests which is written using locust framework to execute performance test please start application using command `locust --host=http://0.0.0.0:8081`, `--host` point to appplication endpoint, afterwards open `http://127.0.0.1:8089` and specify load.




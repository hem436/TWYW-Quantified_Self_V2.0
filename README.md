### Requirements for this application:
1) Python version 3.8.10+ is recommended.
2) Ubuntu 20.4+ or any linux system.
3) node.js v16.16.0 with npm.
4) Redis running at default `localhost:6379`.
5) For Email funtionality add Server email details through which emails will be send in environment variables
    * `SERVER_EMAIL={Youremail}`
    * `EMAIL_PWD={emailpassword}`

### Initialising Project:
* Open terminal with project directory and run `setup.sh` script.
### Running Project:
1) Make sure all requirements are satisfied and project has been initialised successfully.
2) Open terminal in project root directory and run `dev_run.sh` script.

### Running individual apps:
* Flask backend app:
     * Open terminal with `Backend` directory and run `local_run.sh` script
* Flask celery worker app:
    * Open terminal with `Backend` directory and run `local_worker.sh` script
* Flask celery beat app:
    * Open terminal with `Backend` directory and run `local_schedule.sh` script

### Vue Frontend app:
* Open terminal with `Frontend` directory and run command `vue serve` or `npm run serve`

####credits to external sources for this project:
* iconpacks.com for icons svg.
* july.py for heatmap library
* 

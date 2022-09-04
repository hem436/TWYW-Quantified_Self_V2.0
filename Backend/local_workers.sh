#! /bin/sh
echo "======================================================================"
echo "Welcome to to the worker. This will setup the local virtual env."
echo "And then it will start celery worker."
echo "Do not rerun other instances"
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .env/bin/activate
celery -A main.celery worker -l info
# deactivate

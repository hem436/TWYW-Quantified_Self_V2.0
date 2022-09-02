#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"

if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. running setup in new tab"
    gnome-terminal --tab -- bash -c ". ./local_setup.sh;exec bash -i"
fi

# Activate virtual env
. .env/bin/activate
gunicorn main:app --worker-class gevent --bind 127.0.0.1:5000 --workers=4 --reload 
# deactivate

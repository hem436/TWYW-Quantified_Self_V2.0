echo "======================================================================"
echo "Welcome to to the smtp setup. This will setup the smtp server."
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
gnome-terminal --tab -- bash -c "~/go/bin/MailHog;exec bash -i"

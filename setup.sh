echo "======================================================================"
echo "Welcome to to the setup. This will setup both frontend and backend apps."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
cd ./Backend
if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install using pip"
    python3 -m venv .env
fi

# Activate virtual env
. .env/bin/activate

# Upgrade the PIP
pip install --upgrade pip
pip install -r ./requirements.txt
# Work done. so deactivate the virtual env
deactivate
cd ../Frontend
npm install
cd ..

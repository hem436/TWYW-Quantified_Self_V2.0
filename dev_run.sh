#! bin/bash
gnome-terminal --tab -- bash -c "cd ./Backend;. ./local_run.sh;exec bash -i"
gnome-terminal --tab -- bash -c "cd ./Frontend;. ./local_run_frontend.sh;exec bash -i"
gnome-terminal --tab -- bash -c "cd ./Backend;. ./local_workers.sh;exec bash -i"
gnome-terminal --tab -- bash -c "cd ./Backend;. ./local_schedule.sh;exec bash -i"

exit

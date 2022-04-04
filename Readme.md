Author : Mohammad MAZID

This folder contains a python script to find out which of the most common attackable url paths are exposed from a domain, list of all the common known paths is also attached in same folder.


to run this script , we need to first install required packages.

COMMANDS :-

pip install -r requirements.txt

python findattackables.py -d <do.main.name> | tee -a output.log

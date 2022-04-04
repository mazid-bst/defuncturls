##AUTHOR:MOHAMMAD MAZID

import requests
import sys
from optparse import OptionParser
from termcolor import colored

print(sys.argv[2])

paths_file = 'urls.txt'

def pass_options():
    parser = OptionParser()
    parser.add_option("-d", "--domain-name", dest="dns",
                  help="Domain to be scanned")
    (options, args) = parser.parse_args()
    if options.dns:
        dns = options.dns
        discover(dns)
    else:
        parser.error("ERROR : Please parse dns by using -d <abc.xyz.com> or use --help")


def request(dns):
    try:
        if "http://" in dns   or "https://" in dns:
            return requests.get(dns,allow_redirects=False)
        else:
            return requests.get("https://"+dns,allow_redirects=False)
    except requests.exceptions.ConnectionError:
        pass
    except UnicodeError:
        pass


def discover(dns):
    print(colored('[+] Searching Domain:'+dns, 'green'))
    response_in_200 = []
    response_in_301 = []
    response_in_404 = []
    with open(paths_file,"r") as pathlist:
        hiddenpath = 0
        redirectedpath = 0
        notfoundpath = 0
        for line in pathlist:
            word=line.strip()
            target_url=dns+"/"+word
            response=request(target_url)
            response=response.status_code
            if response in range(200,299):
                hiddenpath+=1
                print(colored("Discovered response 200 in --> "+target_url,"red"))
                response_in_200.append(target_url)
            elif response in range(300,310):
                redirectedpath+=1
                print(colored("Discovered response 301,302 in --> "+target_url,"cyan"))
                response_in_301.append(target_url)
            elif response == 404:
                notfoundpath+=1
                print(colored("Discovered response 404 in --> "+target_url,"yellow"))
                response_in_404.append(target_url)
    write_in_file(response_in_200,response_in_301,response_in_404)

def write_in_file(response_in_200,response_in_301,response_in_404):
    file_object = open(sys.argv[2]+'-response_200.txt','w')
    file_object.write(str(response_in_200))
    file_object.close()

    file_object_301 = open(sys.argv[2]+'-response_301.txt','w')
    file_object_301.write(str(response_in_301))
    file_object_301.close()

    file_object_404 = open(sys.argv[2]+'-response_404.txt','w')
    file_object_404.write(str(response_in_404))
    file_object_404.close()

pass_options()
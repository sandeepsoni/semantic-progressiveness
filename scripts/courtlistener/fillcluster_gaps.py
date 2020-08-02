import plac
import ujson
import requests
import os

import sys
if not os.path.abspath ("../../") in sys.path:
	sys.path.append ("../../")

from modules import constants

def make_api_call (url):
	headers = {"Authorization": "Token {0}".format (constants.CL_TOKEN)}
	r = requests.get (url, headers=headers)
	if r.status_code == 200:
		return r.json()
	else:
		print (url, r.status_code)
		return "{}"

@plac.annotations (
	linksfile=("file containining all the links", "positional"),
	dirname=("directory containing the json output", "positional")
)
def main (linksfile, dirname):
	os.makedirs (dirname, exist_ok=True)
	with open (linksfile) as fin:
		for line in fin:
			link = line.strip().split(",")[1]
			js = make_api_call (link)
			if len (js) > 0:
				linkid = link.strip("/").split ("/")[-1]
				fout = open (os.path.join (dirname, "{0}.json".format (linkid)), "w")
				fout.write (ujson.dumps (js) + "\n")
				fout.close()
			else:
				break
				

if __name__ == "__main__":
	plac.call (main)
		

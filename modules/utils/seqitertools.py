import glob
import os

def iter_files (dirname, pattern):
	for filename in sorted (glob.glob (os.path.join (dirname, pattern)), key=lambda x:(len(x), x)):
		yield filename

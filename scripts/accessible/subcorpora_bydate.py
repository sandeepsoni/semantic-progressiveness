import plac
import os

def extract_date_part (ids):
	#/hg191/corpora/historical_newspapers/accessible/TheLiberator/18520109/051.txt
	date_parts = list (map (lambda x:int(os.path.split(x)[0].split("/")[-1]), ids))
	return date_parts

def check_date_condition (start, end, date):
	if len(str (date)) == 8:
		return int(start) <= date and int(end) >= date
	else:
		return int(start[0:6]) <= date and int (end[0:6]) >= date

def writeAfterFilter (start, end, dates, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for i,line in enumerate (fin):
			isOkay = check_date_condition (start, end, dates[i])
			if isOkay:
				fout.write (line)

@plac.annotations(
	start=("the start date", "positional"),
	end=("the end date", "positional"),
	idsfile=("the file containing the filenames", "positional"),
	srcfile=("the file to read", "positional"),
	tgtfile=("the file to write", "positional")
)
def main (start, end, idsfile, srcfile, tgtfile):
	with open (idsfile) as fin:
		ids = [line.strip() for line in fin]


	dates = extract_date_part (ids)

	writeAfterFilter(start, end, dates, srcfile, tgtfile)

if __name__ == "__main__":
	plac.call (main)

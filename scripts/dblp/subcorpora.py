import plac

@plac.annotations(
	lim=("the number of lines", "positional", None, int),
	srcfile=("the file to read", "positional"),
	tgtfile=("the file to write", "positional"),
	tail=("boolean flag for tail of file- True if set", "flag")
)
def main (lim, srcfile, tgtfile, tail):
	with open (srcfile) as fin:
		nlines = len([line for line in fin])
	
	if tail:
		at = nlines - lim
		to = nlines - 1
	else:
		at = 0
		to = lim - 1

	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for i, line in enumerate (fin):
			if i < at: continue
			if i > to: break
			if i >= at:
				fout.write (line)
		

if __name__ == "__main__":
	plac.call (main)

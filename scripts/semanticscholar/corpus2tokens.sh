#!/bin/bash

DIRNAME=/hg190/corpora/academic-data/semantic-scholar

# split the long file into multiple files
split -l 1000000 -a 3 -d $DIRNAME/abstracts.jsonl $DIRNAME/tmpchunks

# tokenize the files in parallel
parallel --max-procs 40 python corpus2tokens.py {} {}.tokenized.jsonl ::: $(ls $DIRNAME/tmpchunks*)

# merge all the files into one (remove the tmp* files)
cat $(ls $DIRNAME/tmpchunks*.tokenized.jsonl | sort) > $DIRNAME/abstracts.tokenized.jsonl
rm $DIRNAME/tmpchunks*

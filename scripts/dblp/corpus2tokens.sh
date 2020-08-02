#!/bin/bash

source constants.sh 

# split the long file into multiple files
split -l 10000 -a 4 -d $FILES_DIR/$CORPUS_FILE $FILES_DIR/tmpchunks

# tokenize the files in parallel
parallel --max-procs 40 python corpus2tokens.py {} {}.tokenized.jsonl ::: $(ls $FILES_DIR/tmpchunks*)

# merge all the files into one (remove the tmp* files)
cat $(ls $FILES_DIR/tmpchunks*.tokenized.jsonl | sort) > $FILES_DIR/$CORPUS_TOKENIZED_FILE
rm -rf $FILES_DIR/tmpchunks*

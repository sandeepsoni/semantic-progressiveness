#!/bin/bash

source constants.sh 

mkdir -p $STATS_DIR

######

## filename: extract the filename of the document (serve as unique identifiers)
## year: extract the year of the document
## newspaper: extract the newspaper of the document.## text: extract the text (without any pre-processing)
## tokens: extract the tokens (separated by whitespace; all tokens lowercase)
## nuniqs: extract the number of unique tokens in the document (all tokens lowercase) 
## ntokens: extract the exact number of tokens in the document
## uncased: extract the tokens (separated by whitespace; original case of the tokens preserved) 

######

parallel python mkstats.py $FILES_DIR/$CORPUS_TOKENIZED_FILE $STATS_DIR {} -prefix $NEWS -start 1827 -end 1865 ::: filename year newspaper text tokens nuniqs ntokens uncased

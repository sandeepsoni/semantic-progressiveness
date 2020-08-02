#!/bin/bash

source constants.sh 

mkdir -p $STATS_DIR
parallel python mkstats.py $FILES_DIR/$CORPUS_TOKENIZED_FILE $STATS_DIR {} -prefix $DBLP ::: id year nauthors abstract nincites tokens noutcites nuniqs ntokens

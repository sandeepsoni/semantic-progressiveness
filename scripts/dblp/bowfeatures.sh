#!/bin/bash

source constants.sh

N=`wc -l $STATS_DIR/$DBLP.id | cut -f 1 -d' '`

python -u bowfeatures.py $STATS_DIR/$DBLP.tokens $STATS_DIR/$DBLP.nincites $STATS_DIR/$DBLP.bowscores $N -nsamples 100000

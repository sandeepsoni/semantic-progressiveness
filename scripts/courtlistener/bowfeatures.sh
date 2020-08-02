#!/bin/bash

source constants.sh

N=`wc -l $STATS_DIR/$OPS.list | cut -f 1 -d' '`

python -u bowfeatures.py $STATS_DIR/$OPS.docs $STATS_DIR/$OPS.ind $STATS_DIR/$OPS.bowscores $N -nsamples 100000

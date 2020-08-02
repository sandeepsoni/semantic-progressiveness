#!/bin/bash

source constants.sh

STATS_DIR=/hg191/corpora/legaldata/data/stats

python corpus2postags.py $STATS_DIR/$OPS.$LIM.early.texts $STATS_DIR/$OPS.$LIM.early.1.pos -seed 100 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.early.texts $STATS_DIR/$OPS.$LIM.early.2.pos -seed 200 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.early.texts $STATS_DIR/$OPS.$LIM.early.3.pos -seed 300 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.early.texts $STATS_DIR/$OPS.$LIM.early.4.pos -seed 400 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.early.texts $STATS_DIR/$OPS.$LIM.early.5.pos -seed 500 -rate $SAMPLING_RATE &
 
python corpus2postags.py $STATS_DIR/$OPS.$LIM.later.texts $STATS_DIR/$OPS.$LIM.later.1.pos -seed 100 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.later.texts $STATS_DIR/$OPS.$LIM.later.2.pos -seed 200 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.later.texts $STATS_DIR/$OPS.$LIM.later.3.pos -seed 300 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.later.texts $STATS_DIR/$OPS.$LIM.later.4.pos -seed 400 -rate $SAMPLING_RATE &
python corpus2postags.py $STATS_DIR/$OPS.$LIM.later.texts $STATS_DIR/$OPS.$LIM.later.5.pos -seed 500 -rate $SAMPLING_RATE &

#!/bin/bash

source constants.sh

parallel --line-buffer python corpus2postags.py $STATS_DIR $DBLP.$LIM.{}.texts -rate $SAMPLING_RATE ::: early later
python mkPoSDistribution.py $STATS_DIR/+.pos $STATS_DIR/$DBLP.$LIM.dist
python mkNounProb.py $STATS_DIR/$DBLP.$LIM.dist $STATS_DIR/$DBLP.$LIM.nounprob
python mkBestTag.py $STATS_DIR/$DBLP.$LIM.dist $STATS_DIR/$DBLP.$LIM.besttag

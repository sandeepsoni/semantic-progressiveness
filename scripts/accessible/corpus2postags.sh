#!/bin/bash

source constants.sh

parallel --line-buffer python corpus2postags.py $STATS_DIR $NEWS.$DATE.{}.texts -rate $SAMPLING_RATE ::: early later
python mkPoSDistribution.py $STATS_DIR/$NEWS.$DATE.+.pos $STATS_DIR/$NEWS.$DATE.dist
python mkNounProb.py $STATS_DIR/$NEWS.$DATE.dist $STATS_DIR/$NEWS.$DATE.nounprob
python mkBestTag.py $STATS_DIR/$NEWS.$DATE.dist $STATS_DIR/$NEWS.$DATE.besttag

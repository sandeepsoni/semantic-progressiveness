#!/bin/bash

source constants.sh

mkdir -p $MODELS_DIR

parallel --line-buffer python text2vectors.py $STATS_DIR/$DBLP.$LIM.{}.docs $MODELS_DIR/$DBLP.$LIM.{}.model ::: early later

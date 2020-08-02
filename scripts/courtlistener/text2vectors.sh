#! /bin/bash

source constants.sh

mkdir -p $MODELS_DIR
parallel --line-buffer python text2vectors.py $STATS_DIR/$OPS.$LIM.{1}.docs $MODELS_DIR/sgns.$LIM.{1}.{2}.model ::: early later ::: 100 200 300 400 500

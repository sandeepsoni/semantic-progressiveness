#!/bin/bash

source constants.sh

mkdir -p $MODELS_DIR

parallel --line-buffer python text2vectors.py $STATS_DIR/$NEWS.$DATE.{}.docs $MODELS_DIR/$NEWS.$DATE.{}.model ::: early later

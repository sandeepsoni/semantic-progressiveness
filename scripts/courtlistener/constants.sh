OPS=ops
LIM=500K #human readable
LIM_NUM=500000
DRIVE=hg191

PARENT_DIR=/$DRIVE/corpora/legaldata/data
FILES_DIR=$PARENT_DIR/files
STATS_DIR=$PARENT_DIR/stats
MODELS_DIR=/$DRIVE/corpora/legaldata/models

CORPUS_FILE=$OPS.jsonl
JURS_FILE=$PARENT_DIR/jurs.names
CORPUS_TOKENIZED_FILE=$OPS.tokenized.jsonl
SAMPLING_RATE=0.2

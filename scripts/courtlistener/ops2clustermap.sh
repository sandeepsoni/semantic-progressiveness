OPINIONS_DIR=/hg190/corpora/courtlistener/opinions
TARGET_DIR=/hg190/corpora/legaldata/data/filemaps
parallel --max-procs 24 python ops2clustermap.py {} $TARGET_DIR ::: $(ls -1d $OPINIONS_DIR/*/ | rev | cut -f 2 -d'/' | rev)

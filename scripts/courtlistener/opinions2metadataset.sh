OUTDIR=/hg190/corpora/legaldata/meta
CLCLUSTERS_DIR=/hg190/corpora/courtlistener/clusters
METADIR=/hg190/corpora/legaldata

# run the basic script on every directory in parallel
mkdir -p $OUTDIR
parallel --max-procs 16 python opinions2meta.py {} $OUTDIR ::: $(ls -d $CLCLUSTERS_DIR/*/)  
wait

#concatenate the files and remove the individial files
cat $OUTDIR/*.jsonl > $METADIR/ops_meta.jsonl
rm -rf $OUTDIR



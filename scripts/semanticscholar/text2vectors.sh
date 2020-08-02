# Run the embeddings model

SRC_DIR=/hg191/corpora/academic-data/semantic-scholar/stats
TGT_DIR=/hg191/corpora/academic-data/semantic-scholar/models

mkdir -p $TGT_DIR
parallel --line-buffer python text2vectors.py $SRC_DIR/abs.2M.{1}.docs $TGT_DIR/sgns.2M.{1}.{2}.model ::: early later ::: 100 200 300 400 500

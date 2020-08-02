# change into the directory of interest and split long files into multiple files
pwd=$PWD
dir=/hg190/corpora/legaldata/sc-docs

cd $dir
split -l 30000 -a 2 -d 0.tokenized.jsonl 0.split.
split -l 30000 -a 2 -d 7.tokenized.jsonl 7.split.

cd $pwd

parallel --max-procs 20 python corpus2postagsparallel.py ::: `ls $dir/*.split.*`
rm $dir/*.split.*

#aggregate and merge all the part of speech files and the delete them
time python mkPoSDistribution.py '/hg190/corpora/legaldata/sc-docs/0.pos.*' $dir/0.p
time python mkBestTag.py $dir/0.p $dir/0.besttag
time python mkNounProb.py $dir/0.p $dir/0.nounprob

time python mkPoSDistribution.py '/hg190/corpora/legaldata/sc-docs/7.pos.*' $dir/7.p
time python mkBestTag.py $dir/7.p $dir/7.besttag
time python mkNounProb.py $dir/7.p $dir/7.nounprob

rm $dir/*.pos.*

mv $dir/0.p $dir/0.pos
mv $dir/7.p $dir 7.pos

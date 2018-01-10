# download the latest English wikipedia dump
curl -L -O "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"

# extract and clean texts from downloaded wikipedia dump
mkdir -p extracted
python WikiExtractor.py enwiki-latest-pages-articles.xml.bz2 -b 1G -o extracted --no-template --processes 24

# process the extracted wiki text corpus including: splitting the sentence, sentence tokenization,
# removing sentences that contain less than 20 characters or less then 5 tokens,
# converting all numerals into 0, say, 1993 converted to 0000
mkdir -p processed
for i in {00..11};
do
	python wiki-corpus-prepare.py extracted/wiki_$i processed/wiki_$i &
done

# merge all the wikipedia text file
cat processed/wiki_* > processed/wiki

# train the word embeddings using skipgram model
mkdir -p results
cd word2vec
./word2vec -train ../processed/wiki -output ../results/enwiki.skip.size300.win10.neg15.sample1e-5.min15.bin -cbow 0 -size 300 -window 10 -negative 15 -hs 0 -sample 1e-5 -threads 24 -binary 1 -min-count 15

# test the performace of word embeddings on word relation test set
./compute-accuracy ../results/enwiki.skip.size300.win10.neg15.sample1e-5.min15.bin < questions-words.txt
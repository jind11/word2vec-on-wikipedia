# word2vec-on-wikipedia
A pipeline for training word embeddings using word2vec on wikipedia corpus.

## How to use
Just run `sudo sh run.sh`, which will:

* Download the latest English wikipedia dump
* Extract and clean texts from the downloaded wikipedia dump
* Pre-process the wikipedia corpus
* Train word2vec model on the processed corpus to produce word embedding results

Details for each step will be discussed as below:

### Wikipedia dump

All the latest English wikipedia can be downloaded from a [Wikipedia database dump](https://dumps.wikimedia.org/enwiki/latest). Here I downloaded all the article pages:

```
curl -L -O "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"
```

### Wikipedia dump extraction

The original wikipedia dump that can be downloaded is in xml format and the structure is quite complex. Thus we need to use a extractor tool to parse it. The one I used is from the [wikiextractor](https://github.com/attardi/wikiextractor) repository. Only the file *WikiExtractor.py* is needed and the descriptions of parameters can be found the in the repository readme file. The output would be each article id and its name followed by the content in text format.

```
python WikiExtractor.py enwiki-latest-pages-articles.xml.bz2 -b 1G -o extracted --no-template --processes 24
```

### Text pre-processing

Before the word2vec training, the corpus needs to be pre-processed, which bascially includes: sentence spltting, sentence tokenization, removing sentences that contain less than 20 characters or 5 tokens, and converting all numerals to 0. For example, "1993" would be converted into "0000". 

```
python wiki-corpus-prepare.py extracted/wiki processed/wiki
```

Here I used [Stanford CoreNLP toolkit 3.8.0](https://stanfordnlp.github.io/CoreNLP/index.html#download) for sentence tokenization. To use it, we need to set up a [local server]((https://stanfordnlp.github.io/CoreNLP/corenlp-server.html)) within the downloaded toolkit folder:

```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```

In the script *wiki-corpus-prepare.py*, I used a [python wrapper](https://github.com/smilli/py-corenlp) of the Stanford CoreNLP server. 

## split texts to sentences
from pycorenlp import StanfordCoreNLP
import re
import time
import sys

stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
nlp = StanfordCoreNLP('http://localhost:9000')

infilePath = sys.argv[1]
outfilePath = sys.argv[2]

splitted_texts = ''
count_articles = 0
count_tokens = 0
start_time = time.time()
outfile = open(outfilePath, 'w')
with open(infilePath, 'r') as f:
    for text in f:
        text = text.strip()
        if len(text) > 20:
            if not text.startswith('<doc id='):
                text = re.sub('\d', '0', text.lower())
                output = nlp.annotate(text, properties={
                                          'annotators': 'ssplit',
                                          'outputFormat': 'json',
                                          'threads': '24',
                                          'tokenize.options': 'normalizeParentheses=false, normalizeOtherBrackets=false'
                                          })
                try:
                    sents = [[token['word'] for token in sent['tokens']] for sent in output['sentences'] if len(sent['tokens']) >= 5]
                except Exception as e:
                    print(e.message, output)
                else:
                    for sent in sents:
                        outfile.write(' '.join(sent)+'\n')
                        count_tokens += len(sent)

            else:
                count_articles += 1
                if count_articles % 2000 == 0:
                    elapsed_time = time.time() - start_time
                    print (infilePath.split('/')[-1], 'Processed article number:', count_articles, 'Elapsed time:', elapsed_time, 's')
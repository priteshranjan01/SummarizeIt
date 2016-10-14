import os
import pdb
import string
import re
import nltk.data
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


def get_sentences(filename, regex):
    with open(filename) as inFile:
        data = inFile.read()
        data = regex.split(data)  # .lower() Is it a good idea to convert to lower?
        sentence = data[1]
    # return sentences, part before that, part before sentences
    return sentence, data[0], data[2]

def sentence_intersection(sent1, sent2):
    #pdb.set_trace()
    sent1 = sent1.lower()
    sent2 = sent2.lower()
    s1 = set(sent1.split())
    s2 = set(sent2.split())
    if len(s1) + len(s2) == 0:
        return 0
    return len(s1.intersection(s2))/((len(s1) + len(s2))/2.0)

def remove_stop_words(sentence):
    #pdb.set_trace()
    #stemmer = PorterStemmer()
    #tokens = word_tokenize(sentence)
    tokens = sentence.split()
    tokens = [i.strip() for i in tokens if i not in string.punctuation]
    #tokens = [stemmer.stem(item) for item in tokens]
    sentence = ' '.join([w for w in tokens if not w.lower() in stopwords.words('english')])
    return sentence

#def calc_sentence_scores()

def parse_files(directory):
    filenames = os.listdir(directory)
    #dataset = []
    regex = re.compile(r'<sentences>([\s\S]*?)<\/sentences>')#, flags=re.DOTALL)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    #pdb.set_trace()
    for filename in filenames:
        print(filename)
        #dataset.append(get_sentences(os.path.join(directory, filename), regex=regex))
        text_para, prefix, suffix = get_sentences(os.path.join(directory, filename), regex=regex)
        sentences = tokenizer.tokenize(text_para)

        sentences = [remove_stop_words(sentence) for sentence in sentences]
        # At this point the sentences won't have stop words
        #pdb.set_trace()
        n = len(sentences)

        vals = [[0 for x in range(n)] for x in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:  # Scope of improvement
                    continue
                #pdb.set_trace()
                vals[i][j] = sentence_intersection(sentences[i], sentences[j])
        #for val in vals: print(val)
        #pdb.set_trace()

        score = []
        #pdb.set_trace()
        for i in xrange(n):
            score.append(sum(vals[i]) - vals[i][i])

        score_sentence = sorted(zip(score, sentences), key=lambda x: x[0], reverse=True)
        #pdb.set_trace()
        for i in range(5):
            print(score_sentence[i][0])
            print (score_sentence[i][1])


if __name__ == "__main__":
    parse_files(directory='trainingHalf')

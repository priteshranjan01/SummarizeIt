from collections import namedtuple
import string
import nltk.data
from nltk.corpus import stopwords


def sentence_intersection(sent1, sent2):
    sent1 = sent1.lower()
    sent2 = sent2.lower()
    s1 = set(sent1.split())
    s2 = set(sent2.split())
    if len(s1) + len(s2) == 0:
        return 0
    return len(s1.intersection(s2))/((len(s1) + len(s2))/2.0)


def remove_stop_words(sentence):
    # stemmer = PorterStemmer()
    # tokens = word_tokenize(sentence)
    tokens = sentence.split()
    tokens = [i.strip() for i in tokens if i not in string.punctuation]
    # tokens = [stemmer.stem(item) for item in tokens]
    sentence = ' '.join([w for w in tokens if not w.lower() in stopwords.words('english')])
    return sentence


def my_text_rank(dataset):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    result = dict()
    for filepath, data in dataset.iteritems():
        text_para = data.text
        sentences = tokenizer.tokenize(text_para)
        sentences = [remove_stop_words(sentence) for sentence in sentences]

        n = len(sentences)
        vals = [[0 for x in range(n)] for x in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:  # Scope of improvement
                    continue
                # pdb.set_trace()
                vals[i][j] = sentence_intersection(sentences[i], sentences[j])
        score = []
        # pdb.set_trace()
        for i in xrange(n):
            score.append(sum(vals[i]) - vals[i][i])
        score_tuple = namedtuple('score_tuple', 'score sentences')
        result[filepath] = [score_tuple(a,b) for a,b in sorted(zip(score, sentences), key=lambda x: x[0], reverse=True)[:5]]

    return result


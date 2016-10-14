from __future__ import print_function

import pdb
import string
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

n_samples = 2000
n_features = 1000
n_topics = 10
n_top_words = 20

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

def get_sentences(filename, regex):
    sentences = []
    with open(filename) as inFile:
        data = inFile.read()
        data = regex.split(data)  # .lower() Is it a good idea to convert to lower?
        sentence = data[1].translate(None, string.punctuation)
        #pdb.set_trace()
    # return sentences, part before that, part before sentences
    return sentence, data[0], data[2]

def run_LDA(dataset):
    print("Extracting tf-idf features for NMF...")
    # Remove words that occur in more than 95% of the documents
    tfidf_vectorizer = TfidfVectorizer(max_features=n_features,
                                       stop_words='english')
    pdb.set_trace()
    tf_idf = tfidf_vectorizer.fit_transform(dataset)

    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_features=n_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(dataset)
    print("Fitting the NMF model with tf-idf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    nmf = NMF(n_components=n_topics, random_state=1,
              alpha=.1, l1_ratio=.5).fit(tf_idf)

    print("\nTopics in NMF model:")
    print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)
    pdb.set_trace()
    print("LDA has been fitted")
    #print("done in %0.3fs." % (time() - t0))
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)


def parse_files(directory):
    filenames = os.listdir(directory)
    dataset = []
    regex = re.compile(r'<sentences>([\s\S]*?)<\/sentences>')#, flags=re.DOTALL)
    for filename in filenames:
        #dataset.append(get_sentences(os.path.join(directory, filename), regex=regex))
        sentence, prefix, suffix = get_sentences(os.path.join(directory, filename), regex=regex)
        dataset.append(sentence)
    return dataset

if __name__ == "__main__":
    dataset = parse_files(directory='trainingHalf')
    run_LDA(dataset)
    pdb.set_trace()

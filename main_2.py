from __future__ import print_function

import pdb
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

n_samples = 2000
n_features = 1000
n_topics = 100
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        pdb.set_trace()
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


def run_LDA(dataset):
    """Copied from example on scikit-learn documentation site"""
    text_data = []
    for data in dataset.values():
        text_data.append(data.text)

    #print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_features=n_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(text_data)
    # nmf = NMF(n_components=n_topics, random_state=1,
    #           alpha=.1, l1_ratio=.5).fit(tf_idf)

    # print("\nTopics in NMF model:")
    # print("Fitting LDA models with tf features, "
    #       "n_samples=%d and n_features=%d..."
    #       % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)
    #pdb.set_trace()
    #print("LDA has been fitted")
    #print("done in %0.3fs." % (time() - t0))
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)


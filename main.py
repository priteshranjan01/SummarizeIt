import os
import re
import pdb
import string
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import xml.etree.ElementTree as ET
from logging import exception

#tree = ElementTree()


# def parse_xml_file(filename):
    # XML Parser not working, fix it
    #parser = ET.XMLParser(encoding="utf-8")
    # pdb.set_trace()
    #
    # print filename
    # root = ET.parse(filename).getroot()

def get_sentences(filename, regex):
    sentences = []
    with open(filename) as inFile:
        data = inFile.read()
        data = regex.split(data)  # .lower() Is it a good idea to convert to lower?
        sentence = data[1].translate(None, string.punctuation)
        #pdb.set_trace()
    # return sentences, part before that, part before sentences
    return sentence, data[0], data[2]

def tokenize(sentence):
    """ Create tokens and remove stop words"""
    #pdb.set_trace()
    stemmer = PorterStemmer()
    tokens = word_tokenize(sentence)
    tokens = [i for i in tokens if i not in string.punctuation]
    tokens = [stemmer.stem(item) for item in tokens]
    tokens = [w for w in tokens if not w in stopwords.words('english')]
    return tokens

def parse_files(directory):
    filenames = os.listdir(directory)
    regex = re.compile(r'<sentences>([\s\S]*?)<\/sentences>')#, flags=re.DOTALL)
    for filename in filenames:
        sentences, pre_data, post_data = get_sentences(os.path.join(directory, filename), regex=regex)
        tokens = tokenize(sentences)
        pdb.set_trace()
        print tokens
        #sentences = parse_xml_file(os.path.join(directory, filename))


if __name__ == "__main__":
    parse_files('trainingHalf')
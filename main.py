import os
import re
import pdb
from collections import namedtuple
from main_3 import my_text_rank, remove_stop_words


def evaluate_summary(dataset, summary):
    """ Compares how many word are common in Catch phrase bag of words and
    summary text bag of words.
    """
    cp_bag_of_words = []
    score_dict = dict()
    for filepath, data in dataset.iteritems():
        cps = data.cps
        for cp in cps:
            cp_bag_of_words += remove_stop_words(cp).split()

        summary_bag_of_words = []
        lines = summary[filepath]
        for line in lines:
            summary_bag_of_words += line.sentences.split()
        s1 = set(cp_bag_of_words)
        s2 = set(summary_bag_of_words)
        common_words = s1.intersection(s2)
        score = len(common_words)/((len(s1)+len(s2))/2.0)
        score_dict[filepath] = score
    return score_dict

def parse_files(directory):
    """ Parse the data hard way.

    python xml parser was throwing an unformed xml exception.
    So I had to do this. Sorry

    And yes, all the files shall be loaded into memory. And all the files in the
    directory have to be of exactly this format."""
    filenames = os.listdir(directory)
    regex_1 = re.compile(r'<name>([\s\S]*?)<\/name>')
    regex_2 = re.compile(r'<AustLII>([\s\S]*?)<\/AustLII>')
    regex_3 = re.compile(r'<catchphrases>([\s\S]*?)<\/catchphrases>')
    regex_31 = re.compile(r'<catchphrase "id=c[0-9]+">([\s\S]*?)<\/catchphrase>')
    regex_4 = re.compile(r'<sentences>([\s\S]*?)<\/sentences>')  # , flags=re.DOTALL)
    data_tuple = namedtuple('data', 'name url cps text')
    dataset = dict()
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        with open(file_path) as inFile:
            data = inFile.read()
            _, name, data = regex_1.split(data)
            _, url, data = regex_2.split(data)
            _, cps, data = regex_3.split(data)
            cps = regex_31.split(cps)[1:len(cps):2]
            _, sentences, _ = regex_4.split(data)
            #pdb.set_trace()
            key = '_'.join(os.path.realpath(file_path).split('\\'))
            #key = '_'.join(file_path.split('\\'))
            dataset[key] = data_tuple(name, url, cps, sentences)
            #pdb.set_trace()
    return dataset

if __name__ == "__main__":

    dataset = parse_files(directory='trainingHalf')
    summary = my_text_rank(dataset)
    result = evaluate_summary(dataset, summary)
    with open('result.txt', 'w') as out_file:
        for file_path, data in dataset.iteritems():
            score = result[file_path]
            #pdb.set_trace()
            res_str = data.name + '\n' + data.url + '\n' + str(score) +'\n\n\n'
            out_file.write(res_str)

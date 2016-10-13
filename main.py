import os
import re
import pdb
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
        sentences = regex.split(data)[1]
        #pdb.set_trace()
    return sentences

def parse_files(directory):
    filenames = os.listdir(directory)
    regex = re.compile(r'<sentences>([\s\S]*?)<\/sentences>')#, flags=re.DOTALL)
    for filename in filenames:
        sentences = get_sentences(os.path.join(directory, filename), regex=regex)

        #sentences = parse_xml_file(os.path.join(directory, filename))


if __name__ == "__main__":
    parse_files('trainingHalf')
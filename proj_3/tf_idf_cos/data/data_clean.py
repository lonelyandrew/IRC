#! /usr/local/bin Python3

import re
from math import log


def remove_html_tags():
    file_list = ['raw_doc/{0}.html'.format(i+1) for i in range(10)]
    new_file_list = ['doc/{0}_.html'.format(i+1) for i in range(10)]
    for i in range(10):
        with open(file_list[i]) as f, \
             open(new_file_list[i], 'w') as nf:
            for line in f.readlines():
                cleaner = re.compile('<.*?>')
                new_str = re.sub(cleaner, '', line)
                new_str = new_str.strip()
                new_str = new_str.lower()
                if new_str:
                    nf.write(new_str + '\n')


def generate_vocabulary():
    file_list = ['doc/{0}_.html'.format(i+1) for i in range(10)]
    words = []
    for file_name in file_list:
        with open(file_name, 'r') as f:
            for line in f.readlines():
                words_in_line = line.split(' ')
                for word in words_in_line:
                    if word.isalnum():
                        if word not in words:
                            words.append(word)
    words.sort()
    counter = 0
    with open('voc.txt', 'w') as v:
        for word in words:
            v.write('{0}:{1}\n'.format(counter, word))
            counter += 1


def generate_tf_table():
    file_list = ['doc/{0}_.html'.format(i+1) for i in range(10)]
    tf_table = {}
    for i in range(10):
        with open(file_list[i], 'r') as f:
            for line in f.readlines():
                words_in_line = line.split(' ')
                for word in words_in_line:
                    if word.isalnum():
                        if word not in tf_table:
                            tf_table[word] = {}
                            tf_table[word][i] = 1
                        elif i not in tf_table[word]:
                            tf_table[word][i] = 1
                        else:
                            tf_table[word][i] += 1
    tf_table = sorted(tf_table.items())
    with open('tf.txt', 'w') as v:
        for term, docs in tf_table:
            for doc, freq in docs.items():
                log_freq = log(freq, 10) + 1
                v.write('{0}:{1}:{2:.2f}\n'.format(term, doc, log_freq))


def generate_idf_table():
    file_list = ['doc/{0}_.html'.format(i+1) for i in range(10)]
    idf_table = {}
    for i in range(10):
        with open(file_list[i], 'r') as f:
            exist_terms = []
            for line in f.readlines():
                words_in_line = line.split(' ')
                for word in words_in_line:
                    if word.isalnum():
                        if word not in exist_terms:
                            if word not in idf_table:
                                idf_table[word] = 1
                            else:
                                idf_table[word] += 1
                            exist_terms.append(word)
    idf_table = sorted(idf_table.items())

    with open('idf.txt', 'w') as t:
        for term, freq in idf_table:
            idf = len(file_list) / freq
            idf = log(idf, 10)
            t.write('{0}:{1:.2f}\n'.format(term, idf))


if __name__ == '__main__':
    # remove_html_tags()
    # generate_vocabulary()
    # generate_tf_table()
    # generate_idf_table()

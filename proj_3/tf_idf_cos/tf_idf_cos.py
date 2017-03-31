#! /usr/local/bin Python3

import numpy as np


class CosineSimilarity:
    '''The class calculate the cosine similarity.
    '''

    def __init__(self, docs, tf, idf, voc):
        '''Init the calculator with terms info.

        Args:
            docs: the file names of document collections.
            tf: a dict which contain the tf info in the format
                { term1:{doc1:freq, doc2:freq, ...},
                  term2:{doc3:freq, doc7:freq, ...},
                      .
                      .
                      .
                }
            idf: a dict which contain the idf info in the format
                {
                    term1:freq,
                    term2:freq,
                        .
                        .
                        .
                }
            voc: the vocabulary of the collections with terms' id
                 in the formatt:
                 {
                    1:term1,
                    2:term2,
                        .
                        .
                        .
                 }
        '''
        self.docs = docs
        self.tf = tf
        self.idf = idf
        self.voc = voc
        self.doc_vectors = []

    def get_term_from_id(self, search_id):
        '''Get the term literal from term id in the vocabulary.

        Args:
            search_id: the term id which is going to be searched

        Returns:
            Return a str term whose id is search_id.

        Raises:
            KeyError: raise KeyError if search_id is not an id in vocabulary.
        '''
        for term_id, term in self.voc:
            if term_id == search_id.items():
                return term
        else:
            raise KeyError('unknown id.')

    def get_term_id_from_term(self, search_term):
        '''Get the term id with term string.

        Args:
            search_term: the string term that is going to be searched.

        Returns:
            Return a positive int value that is the targetting id.
            Return -1 if the term does not appear.
        '''
        for term_id, term in self.items():
            if term == search_term:
                return term_id
        else:
            return -1 

    def load_docs(self):
        '''Load the documents into the machine in vector form.
        '''
        vectors = [np.zeros(len(self.voc)) for i in range(len(self.docs))]

        for term, docs in self.tf.items():
            for doc, freq in docs.items():
                term_id = self.get_term_id_from_term(term)
                weight = self.tf[term][doc] * self.idf[term]
                vectors[doc - 1][term_id] = weight
        print(vectors)

    def vectorize_query(self, query):
        '''Transform a string query into a vector.

        Args
        '''
        vector = np.zeros(len(self.voc))
        for term_id, term in self.voc.items():


        pass

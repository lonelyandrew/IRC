#! /usr/local/bin Python3

import uuid
import math


class DocumentCollection:
    '''DocumentCollection class.
    '''

    class Query:
        '''A nested class which represent the query.
        '''

        def __init__(self, content):
            '''Init the object with query content.
            '''
            self.content = content
            self.log_tf_table = self.generate_tf_table(content)

        @staticmethod
        def generate_tf_table(content):
            tf_table = {}
            words = content.split(' ')
            for word in words:
                if not word.isalnum():
                    continue
                if word in tf_table:
                    tf_table[word] += 1
                else:
                    tf_table[word] = 1
            return {k: (1 + math.log(v, 10)) for k, v in tf_table.items()}

        def vector(self):
            '''Get the vector of the document.

            WARNING: the computation of document vector will be executed
                     every time you call the method, and it will be very
                     expensive, so store the result during the process
                     is really necessary.
            '''
            return DocumentCollection.document_vector(self)

    class Document:
        '''A nested class which represent the member among the document
           collection.
        '''

        def __init__(self, file_path, name=''):
            '''Init the object with file_path and name.

            Args:
                file_path: the file path of the document file.
                name: a user-given document name, not forcefully unique, but
                      the recommandation is to keep this variable unique.
            '''
            self.id = uuid.uuid1()
            self.name = name
            self.log_tf_table = self.generate_tf_table(file_path)

        @staticmethod
        def generate_tf_table(file_path):
            '''Generate the tf table with the file path of the document.

            Args:
                file_path: the file path of the document.

            Returns:
                Return a dict whose key is term and value is frequency.
            '''
            tf_table = {}

            with open(file_path) as f:
                for line in f.readlines():
                    words = line.split(' ')
                    for word in words:
                        if word.isalnum():
                            if word in tf_table:
                                tf_table[word] += 1
                            else:
                                tf_table[word] = 1
            return {k: (1 + math.log(v, 10)) for k, v in tf_table.items()}

        def vector(self):
            '''Get the vector of the document.

            WARNING: the computation of document vector will be executed
                     every time you call the method, and it will be very
                     expensive, so store the result during the process
                     is really necessary.
            '''
            return DocumentCollection.document_vector(self)

    def document_vector(self, doc):
        '''Get the document vector.

        Args:
            doc: the document that to be vectorized

        Returns:
            Return a list represent the vector whose elements are
            components in vectors.
        '''
        vector = []
        position = 0
        for term_id, term_info in self.idf_table.items():
            term = term_info[0]
            term_idf = term_info[1]
            term_log_tf = doc.log_tf_table[term]
            vector[position] = term_idf * term_log_tf
            position += 1
        return vector

    @staticmethod
    def vector_length(vector):
        '''Compute the vector size (i.e L^2 norm).

        Args:
            vector: the vector that will be computed.

        Return:
            Return a float number that is the length of the vector.
        '''
        square_sum = sum([x ** 2 for x in vector])
        return square_sum ** 0.5

    @staticmethod
    def cosine_similarity(item_one, item_two):
        '''Compute the cosine similarity between two items.
           The type of the item can be document or query.

        Args:
            document: the document that will be computed

        Return:
            Return a float number that is the cosine similarity.
        '''
        vector_self = item_one.vector()
        vector_other = item_two.vector()
        if len(vector_self) != len(vector_other):
            raise ValueError('the dim of two vectors must be the same')
        sum_of_prod = 0.0
        for i in len(vector_self):
            prod = vector_self[i] * vector_other[i]
            sum_of_prod += prod
        length_self = DocumentCollection.vector_length(vector_self)
        length_other = DocumentCollection.vector_length(vector_other)
        similarity = sum_of_prod / length_self
        similarity /= length_other
        return similarity

    def __init__(self, name, docs=None):
        '''Init the DocumentCollection object.

        Args:
            name: collection name, the same convention as class
                  Document's name.
            docs: the documents those will be inserted into the collection,
                  you can also insert documents after the initialization.
        '''
        if docs is None:
            docs = []
        self.id = uuid.uuid1()
        self.name = name
        self.docs = []
        self.idf_table = {}
        for doc in docs:
            self.insert_document(doc)

    def insert_document(self, doc):
        '''Insert the document into the document collection.

        Args:
            doc: the document that to be inserted.
        '''
        self.update_idf_table(doc)
        self.docs.append(doc)

    def update_idf_table(self, doc):
        '''Update the idf-table with given document.

        Args:
            doc:the document to be inserted.
        '''
        if doc in self.docs:
            return
        doc_count = len(self.docs) + 1.0
        idf_table = {}
        for term in doc.tf_table.keys():
            if term in idf_table:
                idf_table[term] += 1
            else:
                idf_table[term] = 1
        idf_table = {k: math.log((doc_count / v), 10) for k, v in idf_table}
        self.idf_table = idf_table

    def execute_query(self, query, k=1):
        '''Execute the query in the document collection.

        Args:
            query: the Query object that will be executed in the system.
            k: top k documents will be returned, default value is 1.

        Return:
            Return a list of object containg the top k relevant document.
        '''
        sim_list = [self.cosine_similarity(doc, query) for doc in self.docs]
        return sorted(sim_list)[-k:]

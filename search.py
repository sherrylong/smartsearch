import json
from pprint import pprint
import os
import time
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class Search:
    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200')
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self):
        self.es.indices.delete(index='my_documents', ignore_unavailable=True)
        self.es.indices.create(index='my_documents')

    def insert_document(self, document):
        return self.es.index(index='my_documents', body=document)
    
    def insert_documents(self, documents, batch_size=100):
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        for batch in chunks(documents, batch_size):
            operations = []
            for document in batch:
                operations.append({'index': {'_index': 'my_documents'}})
                operations.append(document)
            self.es.bulk(operations=operations)
    
    def parse_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        documents = []
        fields = ['title', 'description', 'user_categories']
        for item in root.findall('grant'):
            document = {}
            for field in fields:
                element = item.find(field)
                if element is not None:
                    document[field] = element.text
            documents.append(document)
        return documents

    def reindex(self):
        self.create_index()
        documents = self.parse_xml('grants-data.xml')
        self.insert_documents(documents)
    
    def search(self, **query_args):
        return self.es.search(index='my_documents', **query_args)
    
    def retrieve_document(self, id):
        return self.es.get(index='my_documents', id=id)

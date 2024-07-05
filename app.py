import re
from flask import Flask, render_template, request
from search import Search

app = Flask(__name__)
es = Search()


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/')
def handle_search():
    query = request.form.get('query', '')
    from_ = request.form.get('from_', type=int, default=0)
    results = es.search(
        query={
            'multi_match': {
                'query': query,
                'fields': ['title', 'description', 'user_categories'],
            }
        }, size=5, from_=from_
    )
    return render_template('index.html', results=results['hits']['hits'],
                           query=query, from_=from_,
                           total=results['hits']['total']['value'])




@app.get('/document/<id>')
def get_document(id):
    document = es.retrieve_document(id)
    title = document['_source']['title']
    paragraphs = document['_source']['description'].split('\n')
    paragraphs.append('Categories: ' + document['_source']['user_categories'])
    return render_template('document.html', title=title, paragraphs=paragraphs)

@app.cli.command()
def reindex():
    """Regenerate the Elasticsearch index."""
    response = es.reindex()
    print('Reindex success')
    # print(f'Index with {len(response["items"])} documents created '
    #       f'in {response["took"]} milliseconds.')

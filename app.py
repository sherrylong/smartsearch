import re, os
from flask import Flask, render_template, request, session, redirect, url_for
from src.rewrite_query import rewrite_query
from src.search import Search

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
es = Search()


@app.get('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def submit_search():
    if request.method == 'POST':
        query = request.form.get('query', '')
        session['query'] = query
        return redirect(url_for('search_results', query=query, from_=0))
    return render_template('index.html')


@app.route('/search_results')
def search_results():
    query = request.args.get('query', '')
    from_ = request.args.get('from_', type=int, default=0)
    
    if query:
        if 'query' in session and session['query'] == query:
            modified_query = session.get('modified_query', '')
        else:
            modified_query = rewrite_query(query)
            session['modified_query'] = modified_query
            session['modified_query'] = modified_query
            session['query'] = query

    results = es.search(
        query={
            'multi_match': {
                'query': modified_query,
                'fields': ['title', 'description', 'user_categories'],
            }
        }, 
        highlight={
            'pre_tags': ['<strong>'],
            'post_tags': ['</strong>'],
            'fields': {
                'description': {
                    'fragment_size': 300,
                    'number_of_fragments': 1,
                }
            }
        },
        size=5, from_=from_
    )
    return render_template('index.html', results=results['hits']['hits'],
                           query=query, modified_query=modified_query, from_=from_,
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

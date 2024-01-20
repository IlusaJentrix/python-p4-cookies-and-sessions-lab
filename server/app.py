from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Your logic for retrieving and rendering a list of articles goes here
    articles = Article.query.all()
    article_list = [{'id': article.id, 'title': article.title} for article in articles]
    return jsonify({'articles': article_list})

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize session['page_views'] to 0 if it's the first request
    session['page_views'] = session.get('page_views', 0)

    # Increment the value of session['page_views'] by 1
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        # Render a JSON response with the article data
        article = Article.query.get(id)
        if article:
            return jsonify({'id': article.id, 'title': article.title, 'content': article.content})
        else:
            return jsonify({'message': 'Article not found'}), 404
    else:
        # Render a JSON response with an error message and status code 401
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)


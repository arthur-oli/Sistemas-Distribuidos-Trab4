from flask import Flask, jsonify, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_sse import sse
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

db = SQLAlchemy(app)
CORS(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year_published': self.year_published
        }

with app.app_context():
    db.create_all()

interests = []

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], year_published=data['year_published'])
    db.session.add(new_book)
    db.session.commit()
    check_interests(new_book)
    return jsonify(new_book.to_json()), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_json())

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    book.title = data['title']
    book.author = data['author']
    book.year_published = data['year_published']
    db.session.commit()
    return jsonify(book.to_json())

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/interest', methods=['POST'])
def add_interest():
    data = request.json
    newInterest = {
        'name': data['clientName'],
        'interest_type': data['choice'],
        'interest': data['message']
    }

    interests.append(newInterest)

    return jsonify({"message": "Interesse registrado com sucesso", "sse_url": url_for('event_stream')}), 201

def check_interests(book):
    for interest in interests:
        if ((interest.interest_type == "titulo" and interest.interest in book.title) or (interest.interest_type == "author" and interest.interest in book.author)):
            sse.publish(
                {"title": book.title, "author": book.author, "year_published": book.year_published}, type = "interest"
            )

@app.route('/stream', methods=['POST'])
def event_stream():
    def generate():
        pubsub = sse._redis.pubsub()
        pubsub.subscribe("interest")
        for message in pubsub.listen():
            bMessage = str.encode(message)
            key = RSA.import_key(open('private_key.der').read())
            h = SHA256.new(message)
            signature = pkcs1_15.new(key).sign(h)
            yield "data: {}, {}, {}\n\n".format(message, h, signature)

    return generate()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
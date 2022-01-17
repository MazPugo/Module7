from flask import Flask, jsonify, abort, make_response, request
from model import books
import sys


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(books.all())

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_todo(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})

@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or not 'name' in request.json:
        print('This is error output', file=sys.stderr)
        abort(400)
    data = request.json    
    book = {
        'id': books.all()[-1]['id'] + 1,
        'name': data.get('name'),
        'author': data.get('author')
    }
    books.create(book)
    return jsonify({'book': book}), 201

@app.route("/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'name' in data and not isinstance(data.get('name'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'covercolor' in data and not isinstance(data.get('covercolor'), str),
        'page' in data and not isinstance(data.get('page'), int),
    ]):
        abort(400)
    book = {
        'id': book_id,
        'name': data.get('name', book['name']),
        'author': data.get('author', book['author']),
        'covercolor': data.get('covercolor', book['covercolor']),
        'page': data.get('page', book['page'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

@app.route("/api/v1/books/sortbycolor", methods=['GET'])
def sort_book_covercolor():
    for i in books.all():
     entries = sorted(books.all(),key=lambda d: d['covercolor'])
     if not entries:
        abort(404)
     return jsonify({'entries': entries})
 
@app.route("/api/v1/books/sortbypage", methods=['GET'])
def sort_book_page():
    for i in books.all():
     entries = sorted(books.all(),key=lambda d: d['page'])
     if not entries:
        abort(404)
     return jsonify({'entries': entries})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)


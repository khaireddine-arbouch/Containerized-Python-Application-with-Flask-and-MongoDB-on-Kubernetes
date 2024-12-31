from flask import Flask, jsonify, request, abort
from pymongo import MongoClient, errors
import json
import os

# Prepare MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set.")
print("mongo_uri: ", mongo_uri)

client = None
try:
    client = MongoClient(mongo_uri)
    database = client["bookstoredatabase"]
    collection = database["bookstorecollection"]
except errors.ConnectionFailure as e:
    print("Could not connect to MongoDB:", e)
    raise

# Prepare Flask app
app = Flask(__name__)

@app.route("/books", methods=["GET"])
def get_all_books():
    try:
        books = list(collection.find({}, {"_id": 0}))  # Exclude _id field
        return jsonify(books), 200
    except Exception as e:
        abort(500, description="Error fetching books: " + str(e))

@app.route("/books/restore", methods=["POST"])
def restore_all_books():
    try:
        # Drop the current collection and restore from bookstore.json
        collection.drop()
        with open("bookstore.json") as f:
            books = json.load(f)
        collection.insert_many(books)
        return jsonify({"message": "Books restored successfully!"}), 200
    except Exception as e:
        abort(500, description="Error restoring books: " + str(e))

@app.route("/books", methods=["POST"])
def add_book():
    book = request.get_json()

    if not book or not all(key in book for key in ["isbn", "title", "author", "year", "price"]):
        abort(400, description="Missing required book data.")

    try:
        collection.insert_one(book)
        return jsonify({"message": "Book added successfully!"}), 201
    except Exception as e:
        abort(500, description="Error adding book: " + str(e))

@app.route("/books/<book_isbn>", methods=["GET"])
def get_book(book_isbn):
    book = collection.find_one({"isbn": book_isbn}, {"_id": 0})  # Exclude _id field

    if book:
        return jsonify(book), 200
    else:
        abort(404, description="Book not found.")

@app.route("/books/<book_isbn>", methods=["PUT"])
def update_book(book_isbn):
    book = request.get_json()

    if not book or not all(key in book for key in ["isbn", "title", "author", "year", "price"]):
        abort(400, description="Missing required book data.")

    try:
        result = collection.update_one(
            {"isbn": book_isbn},
            {"$set": book}
        )

        if result.matched_count > 0:
            return jsonify({"message": "Book updated successfully!"}), 200
        else:
            abort(404, description="Book not found.")

    except Exception as e:
        abort(500, description="Error updating book: " + str(e))

@app.route("/books/<book_isbn>", methods=["DELETE"])
def delete_book(book_isbn):
    try:
        result = collection.delete_one({"isbn": book_isbn})

        if result.deleted_count > 0:
            return jsonify({"message": "Book deleted successfully!"}), 200
        else:
            abort(404, description="Book not found.")
    except Exception as e:
        abort(500, description="Error deleting book: " + str(e))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

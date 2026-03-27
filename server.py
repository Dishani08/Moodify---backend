from flask import Flask, send_from_directory
import logging

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    logging.info("Serving on http://localhost:8000")
    app.run(host='127.0.0.1', port=8000, debug=True)
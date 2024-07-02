from flask import Flask, request, redirect, jsonify
import string
import random

app = Flask(__name__)

url_mappings = {}
base_url = "http://localhost:5000/"

def generate_unique_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    while short_url in url_mappings:
        short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route('/shorten', methods=['POST'])
def shorten_url_handler():
    data = request.get_json()
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({"error": "No URL provided"}), 400
    short_url = generate_unique_short_url()
    url_mappings[short_url] = long_url
    return jsonify({"short_url": base_url + short_url})

@app.route('/<short_url>', methods=['GET'])
def redirect_to_long_url_handler(short_url):
    long_url = url_mappings.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"error": "URL not found"}), 404

@app.route('/urls', methods=['GET'])
def get_url_mappings_handler():
    return jsonify(url_mappings)

if __name__ == "__main__":
    app.run(debug=True)

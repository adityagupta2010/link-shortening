from flask import Flask, request, jsonify, redirect
import random
import string

# Initialize Flask app
app = Flask(__name__)

# Dictionary to store shortened URLs
url_mapping = {}

# Function to generate a random short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Route to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')

    if not long_url:
        return jsonify({'error': 'Missing long_url'}), 400

    # Generate a unique short code
    short_code = generate_short_code()
    while short_code in url_mapping:
        short_code = generate_short_code()

    # Save mapping
    url_mapping[short_code] = long_url

    # Return shortened URL
    return jsonify({'short_url': f'http://localhost:5000/{short_code}'})

# Route to redirect to the original URL
@app.route('/<short_code>')
def redirect_to_url(short_code):
    long_url = url_mapping.get(short_code)

    if long_url:
        return redirect(long_url)
    else:
        return jsonify({'error': 'Short URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

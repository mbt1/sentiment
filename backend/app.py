from flask import Flask, render_template, jsonify
from mastodon import Mastodon
import os

mastodon = Mastodon(
    access_token=os.environ.get('MASTODON_SENTIMENT_MASTODON_API_KEY'),
    api_base_url='https://mas.to/'  # Replace with the Mastodon instance URL
)

app = Flask(__name__)

@app.route('/api/public_toots', methods=['GET'])
def get_public_toots():
    public_toots = mastodon.timeline_public()
    return jsonify(public_toots)

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

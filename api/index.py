# https://github.com/vercel/examples/tree/main/python/flask3
# https://stackoverflow.com/a/33468993
# https://stackoverflow.com/a/31684470

from flask import Flask
from dotenv import load_dotenv
import pusher
import os

load_dotenv()
app_id=os.getenv('app_id')
key=os.getenv('key')
secret=os.getenv('secret')
cluster=os.getenv('cluster')

app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"""
        <!DOCTYPE html>
        <head>
        <title>Pusher Test</title>
        <script src="https://js.pusher.com/8.4.0/pusher.min.js"></script>
        <script>
            var pusher = new Pusher('{key}', {{
            cluster: '{cluster}'
            }});

            var channel = pusher.subscribe('my-channel');
            channel.bind('my-event', function(data) {{
            alert(JSON.stringify(data));
            }});
        </script>
        </head>
        <body>
        <h1>Pusher Test</h1>
        <p>
            Try publishing an event to channel <code>my-channel</code>
            with event name <code>my-event</code>.
        </p>
        </body>
    """

@app.route("/send")
def send():
    pusher_client = pusher.Pusher(app_id, key, secret, cluster=cluster, ssl=True)
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    return "<p>Message sent</p>"
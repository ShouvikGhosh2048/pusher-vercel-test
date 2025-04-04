# https://github.com/vercel/examples/tree/main/python/flask3
# https://stackoverflow.com/a/33468993
# https://stackoverflow.com/a/31684470

from flask import Flask, request
from dotenv import load_dotenv
import pusher
import os
import json

load_dotenv()
app_id=os.getenv('app_id')
key=os.getenv('key')
secret=os.getenv('secret')
cluster=os.getenv('cluster')

pusher_client = pusher.Pusher(app_id, key, secret, cluster=cluster, ssl=True)

app = Flask(__name__)

@app.route("/")
def home():
    return f"""
        <!DOCTYPE html>
        <head>
        <title>Pusher Test</title>
        <script src="https://js.pusher.com/8.4.0/pusher.min.js"></script>
        <script>
            let token = '';

            let pusher = new Pusher('{key}', {{
                cluster: '{cluster}'
            }});
            let channel = null;

            function generateRandomToken() {{
                const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                let s = '';
                for (let i = 0; i < 20; i++) {{
                    s = s + chars[Math.floor(Math.random() * chars.length)];
                }}
                return s;
            }}

            function getInputToken() {{
                return document.querySelector("#tokenInput").value;
            }}

            function setToken(newToken) {{
                if (newToken === "") {{ return; }}

                if (channel !== null) {{ pusher.unsubscribe('private-' + token); }}
                channel = pusher.subscribe('private-' + newToken);
                channel.bind('message', function(data) {{
                    const messagesDiv = document.querySelector("#messages");
                    messagesDiv.innerText += JSON.stringify(data);
                }});

                token = newToken;
                document.querySelector('#token').innerText = 'Token: ' + token;
            }}

            function sendMessage() {{
                const message = document.querySelector("#messageInput").value;
                if (token === "" || message === "") {{ return; }}
                fetch('/send/' + token, {{
                    'method': 'POST',
                    'body': JSON.stringify({{ "message": message }}),
                    'headers': {{ 'Content-Type': 'application/json' }}
                }});
            }}
        </script>
        </head>
        <body>
            <div><button onclick="setToken(generateRandomToken())">Generate token</button> or <input id="tokenInput" placeholder="Token"/><button onclick="setToken(getInputToken())">Use</button></div>
            <span id="token">Token:</span>
            <div><input id="messageInput" placeholder="Message"/><button onclick={{sendMessage()}}>Send</button></div>
            <div id="messages"></div>
        </body>
    """

@app.post("/send/<token>")
def send(token):
    pusher_client.trigger('private-' + token, 'message', { 'token': token, 'message': request.json['message'] })
    return "<p>Message sent</p>"

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():

  # Keeping this for now since this just a test project.
  # This authenticates every user. Don't do this in production!
  auth = pusher_client.authenticate(
    channel=request.form['channel_name'],
    socket_id=request.form['socket_id']
  )
  return json.dumps(auth)
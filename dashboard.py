from flask import Flask, redirect, request, session
import requests, os

app = Flask(__name__)
app.secret_key = "secret"

CID = os.getenv("CLIENT_ID")
SEC = os.getenv("CLIENT_SECRET")
RED = os.getenv("REDIRECT_URI")

API = "https://discord.com/api"

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    guilds = session["guilds"]

    html = "<h1>Your Servers</h1>"
    for g in guilds:
        if g["owner"] or (int(g["permissions"]) & 0x8):
            html += f"<p>{g['name']}</p>"

    return html

@app.route("/login")
def login():
    return redirect(f"{API}/oauth2/authorize?client_id={CID}&redirect_uri={RED}&response_type=code&scope=identify guilds")

@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": CID,
        "client_secret": SEC,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": RED
    }

    token = requests.post(f"{API}/oauth2/token", data=data).json()["access_token"]

    user = requests.get(f"{API}/users/@me", headers={"Authorization": f"Bearer {token}"}).json()
    guilds = requests.get(f"{API}/users/@me/guilds", headers={"Authorization": f"Bearer {token}"}).json()

    session["user"] = user
    session["guilds"] = guilds

    return redirect("/")

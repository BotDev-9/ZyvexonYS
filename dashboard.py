from flask import Flask, redirect, request, session
import requests, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

API = "https://discord.com/api"

# Home
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    guilds = session["guilds"]

    html = f"<h1>Welcome {user['username']}</h1><h2>Your Servers:</h2>"

    for g in guilds:
        # Show only servers where user is admin
        if g["owner"] or (int(g["permissions"]) & 0x8):
            html += f"<p>{g['name']}</p>"

    return html


# Login
@app.route("/login")
def login():
    return redirect(
        f"{API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20guilds"
    )


# Callback
@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Get token
    r = requests.post(f"{API}/oauth2/token", data=data, headers=headers)
    token = r.json().get("access_token")

    if not token:
        return "OAuth failed"

    # Get user
    user = requests.get(
        f"{API}/users/@me",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    # Get guilds
    guilds = requests.get(
        f"{API}/users/@me/guilds",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    session["user"] = user
    session["guilds"] = guilds

    return redirect("/")
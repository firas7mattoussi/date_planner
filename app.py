from flask import Flask, request, redirect, url_for, render_template_string, abort
import secrets

app = Flask(__name__)

INVITES = {}

HEADLINES = [
    "Please demonstrate basic planning skills."
]

LANDING_TEMPLATE = """
<!doctype html>
<html>s
  <head>
    <meta charset="utf-8" />
    <title>Date Planner</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
             background: #0b0b10; color: #f2f2f7;
             display:flex; align-items:center; justify-content:center;
             min-height:100vh; margin:0; }
      .card { width: min(560px, 92vw); background:#141420;
              border:1px solid #2a2a40; border-radius:18px;
              padding:26px; box-shadow: 0 10px 30px rgba(0,0,0,.35); }
      h1 { font-size: 1.35rem; margin:0 0 16px; line-height:1.25; }
      p { margin: 0 0 18px; color:#c9c9d6; }
      .row { display:flex; gap:12px; flex-wrap:wrap; }
      button { flex:1; min-width: 180px; padding:14px 16px;
               border-radius:14px; border:0; cursor:pointer;
               font-weight:700; font-size:1rem; }
      .ok { background:#7c5cff; color:white; }
      .nope { background:#2b2b3f; color:#f2f2f7; border:1px solid #3a3a55; }
      .small { margin-top:14px; font-size:.9rem; color:#a8a8b8; }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>{{ headline }}</h1>
      <p>
        Hi.
        I’ve planned the last few dates.  
        This time, you’re doing it.
      </p>

      <div class="row">
        <form method="post" action="{{ url_for('continue_invite', token=token) }}">
          <button class="ok" type="submit">I accept responsibility</button>
        </form>

        <form method="post" action="{{ url_for('give_up', token=token) }}">
          <button class="nope" type="submit">I refuse to choose</button>
        </form>
      </div>

      <div class="small">
        This page is legally allowed to bully you.
      </div>
    </div>
  </body>
</html>
"""

FORM_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Pick the Details</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
             background: #0b0b10; color: #f2f2f7;
             display:flex; align-items:center; justify-content:center;
             min-height:100vh; margin:0; }
      .card { width: min(560px, 92vw); background:#141420;
              border:1px solid #2a2a40; border-radius:18px;
              padding:26px; box-shadow: 0 10px 30px rgba(0,0,0,.35); }
      h1 { font-size: 1.25rem; margin:0 0 16px; }
      label { display:block; margin: 14px 0 6px; color:#c9c9d6; }
      input { width:100%; padding:12px 12px;
              border-radius:12px; border:1px solid #3a3a55;
              background:#0f0f18; color:#f2f2f7; font-size:1rem; }
      button { margin-top:16px; width:100%;
               padding:14px 16px; border-radius:14px; border:0;
               cursor:pointer; font-weight:800; font-size:1rem;
               background:#7c5cff; color:white; }
      .small { margin-top:12px; font-size:.9rem; color:#a8a8b8; }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>Good.</h1>

      <form method="post" action="{{ url_for('submit', token=token) }}">
        <label for="time">Time</label>
        <input id="time" name="time" required placeholder="A real time. With numbers." />

        <label for="place">Place</label>
        <input id="place" name="place" required placeholder="An actual location. Not 'wherever'." />

        <button type="submit">Lock it in</button>
      </form>

      <div class="small">
        Decide and I'll think about it.
      </div>
    </div>
  </body>
</html>
"""

THANKS_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Submitted</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
             background: #0b0b10; color: #f2f2f7;
             display:flex; align-items:center; justify-content:center;
             min-height:100vh; margin:0; }
      .card { width: min(560px, 92vw); background:#141420;
              border:1px solid #2a2a40; border-radius:18px;
              padding:26px; box-shadow: 0 10px 30px rgba(0,0,0,.35); }
      h1 { margin:0 0 12px; font-size:1.25rem; }
      .pill { display:inline-block; padding:8px 10px;
              border-radius:999px; background:#0f0f18;
              border:1px solid #3a3a55; margin: 6px 6px 0 0; }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>Wow. Growth.</h1>
      <div class="pill">🕒 {{ time }}</div>
      <div class="pill">📍 {{ place }}</div>
      <p style="margin-top:14px; color:#c9c9d6;">
        Screenshot this and send it to me.  
        I will pretend I’m not impressed.
      </p>
    </div>
  </body>
</html>
"""

@app.get("/new")
def new_invite():
    token = secrets.token_urlsafe(10)
    INVITES[token] = {"submitted": False, "time": "", "place": ""}
    invite_url = url_for("invite", token=token, _external=True)
    return f"""
    <h2>Link generated.</h2>
    <p>Send this. Don’t explain it.</p>
    <p><a href="{invite_url}">{invite_url}</a></p>
    """

@app.get("/invite/<token>")
def invite(token):
    if token not in INVITES:
        abort(404)
    headline = secrets.choice(HEADLINES)
    return render_template_string(LANDING_TEMPLATE, token=token, headline=headline)

@app.post("/invite/<token>/continue")
def continue_invite(token):
    if token not in INVITES:
        abort(404)
    return render_template_string(FORM_TEMPLATE, token=token)

@app.post("/invite/<token>/giveup")
def give_up(token):
    if token not in INVITES:
        abort(404)
    return redirect("https://www.wikihow.com/Be-Happy-Being-Single")

@app.post("/invite/<token>/submit")
def submit(token):
    if token not in INVITES:
        abort(404)

    time = request.form.get("time", "").strip()
    place = request.form.get("place", "").strip()

    INVITES[token]["submitted"] = True
    INVITES[token]["time"] = time
    INVITES[token]["place"] = place

    return render_template_string(THANKS_TEMPLATE, time=time, place=place)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
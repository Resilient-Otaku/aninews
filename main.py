from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Aninews</title>
      <style>
        body {
          background: #080b18;
          color: white;
          font-family: Arial;
          text-align: center;
          padding: 50px 15px;
        }
        h1 { color: #a78bfa; font-size: 38px; }
        p { color: #cbd5e1; }
        button {
          background: linear-gradient(90deg,#9333ea,#2563eb);
          color: white;
          border: 0;
          padding: 14px 25px;
          border-radius: 12px;
          font-size: 16px;
        }
      </style>
    </head>
    <body>
      <h1>🌌 ANINEWS</h1>
      <h2>Welcome to the Animeverse!</h2>
      <p>Discover. Explore. Connect.</p>
      <button>Explore Anime</button>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()

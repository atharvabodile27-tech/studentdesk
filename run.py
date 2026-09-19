"""
StudentDesk - application entry point.
Run:  python run.py
"""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    # host=0.0.0.0 zaroori hai Docker/cloud ke liye
    app.run(host="0.0.0.0", port=port, debug=debug)

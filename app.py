from flask import Flask
from routes import register_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
register_routes(app)
    
if __name__ == '__main__':
    if os.getenv('DEBUG_MODE', 'False') == 'True':
        app.run(host='0.0.0.0', port=5005, debug=True)
    else:
        app.run()
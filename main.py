from dotenv import load_dotenv
import os

load_dotenv()

from website import create_app

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode)

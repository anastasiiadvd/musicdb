#create instance of app for application
from app import app

#allow the site to be started with: python run.py
if __name__ == "__main__":
    app.run(debug=True)

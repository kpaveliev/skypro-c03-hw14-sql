from flask import Flask, render_template

# Initiate Flask app, load config
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Start app
if __name__ == '__main__':
    app.run()


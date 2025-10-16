from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, we are done with jenkins, going to start terraform."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

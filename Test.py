from flask import Flask, send_from_directory, redirect

app = Flask(__name__)


@app.route('/')
def download():
    return redirect("vmanager://web?url=http://www.baidu.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
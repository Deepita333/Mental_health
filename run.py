from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text_response')
def text_response():
    subprocess.Popen(["python", "app/ap1.py"])
    return redirect(url_for('index'))

@app.route('/audio_response')
def audio_response():
    subprocess.Popen(["python", "app/ap.py"])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

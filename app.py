from flask import Flask, session, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello, World!</p>"




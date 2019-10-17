from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


app.run()

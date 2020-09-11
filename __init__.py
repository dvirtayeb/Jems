from flask import Flask
import Config

app = Flask(__name__)
app.config.from_object(Config)

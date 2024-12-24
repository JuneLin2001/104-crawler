from flask import Flask
from flask_cors import CORS
from controllers.job_controller import job_controller

app = Flask(__name__)
CORS(app)

app.register_blueprint(job_controller)

if __name__ == "__main__":
    app.run(debug=True)

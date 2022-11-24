from hashlib import new
from db import db
from flask import Flask
from db import Course
from db import User
from db import Assignment
import json
from flask import request
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
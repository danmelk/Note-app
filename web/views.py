import re
from types import MethodDescriptorType
from flask import Blueprint, render_template
from flask.globals import request
from flask.helpers import url_for
from werkzeug.utils import redirect

views = Blueprint('views', __name__)

@views.route('/home', methods=['POST', 'GET'])
def home():
    pass

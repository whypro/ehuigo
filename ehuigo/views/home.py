# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app


home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html')


@home.route('/eval/')
def eval():
    return render_template('eval.html')

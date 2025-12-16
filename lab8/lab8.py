# lab8.py

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import path
import re

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8')
def main():
    """Главная страница лабораторной работы 8"""
    # Пока будем отображать "anonymous", потом добавим авторизацию
    username = session.get('login', 'anonymous')
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/login')
def login():
    """Страница входа"""
    return render_template('lab8/login.html')

@lab8.route('/lab8/register')
def register():
    """Страница регистрации"""
    return render_template('lab8/register.html')

@lab8.route('/lab8/articles')
def articles():
    """Страница со списком статей"""
    username = session.get('login', 'anonymous')
    # Здесь позже будет загрузка статей из БД
    return render_template('lab8/articles.html', username=username)

@lab8.route('/lab8/create')
def create_article():
    """Страница создания статьи"""
    username = session.get('login', 'anonymous')
    return render_template('lab8/create.html', username=username)

# Заглушки для POST-запросов (будут реализованы позже)
@lab8.route('/lab8/login', methods=['POST'])
def login_post():
    return redirect('/lab8')

@lab8.route('/lab8/register', methods=['POST'])
def register_post():
    return redirect('/lab8')

@lab8.route('/lab8/create', methods=['POST'])
def create_post():
    return redirect('/lab8/articles')
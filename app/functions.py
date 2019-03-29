from flask import request, url_for
from app.models import Mat1tests
import random


def random_bg_picture():
    pictures = [
    "../static/bg02.jpg",
    "../static/bg01.jpg",
    "../static/bg03.jpg",
    "../static/bg04.jpg",
    "../static/bg05.jpg",
    "../static/bg06.jpg",
    "../static/bg07.jpg",
    "../static/bg08.jpg",
    "../static/bg09.jpg"
    ]

    random_picture = random.choice(pictures)

    return random_picture


def procent(a, b):
    try:
        resultat = a / b * 100
        return resultat
    except ZeroDivisionError:
        return 0


def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')


import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = 'xcdqtE3tbZJmY5B'

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="mattool",
    password="kWdqtC9tbRJmY6B",
    hostname="mattool.mysql.pythonanywhere-services.com",
    databasename="mattool$mattool",
    )

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER= 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'siri.padkjaer@gmail.com'
    MAIL_PASSWORD = 'ryn67qjn'
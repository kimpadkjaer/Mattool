from flask import render_template
from app import app, db
import logging

@app.errorhandler(404)
def not_found_error(error):
    logger = logging.getLogger(__name__)
    logger.warn("404")
    return render_template('404.html', title="MAT | Retteværktøj: 404 - Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger = logging.getLogger(__name__)
    logger.warn("500")
    return render_template('500.html', title="MAT | Retteværktøj: 500 - En uventet fejl er opstået"), 500
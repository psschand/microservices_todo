
import sys
import unittest
from logging.config import dictConfig
from datetime import datetime
# import coverage
from flask.cli import FlaskGroup
from src import create_app, db
from src.models.task import Task

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
# COV = coverage.coverage(
#     branch=True,
#     include='src/*',
#     omit=[
#         'tests/*',
#         'src/config.py',
#     ]
# )
# COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)

import pytest
@cli.command()
def test():
    """Runs the tests without code coverage"""
   
    # pytest can run unit tests
    pytest.main(["-v", "tests"])
    
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


# @cli.command()
# def cov():
#     """Runs the unit tests with coverage."""
#     tests = unittest.TestLoader().discover('tests')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         COV.stop()
#         COV.save()
#         print('Coverage Summary:')
#         COV.report()
#         COV.html_report()
#         COV.erase()
#         return 0
#     sys.exit(result)
    
@cli.command('populate_db')
def populate_db():
    """Populate the database with report."""

    db.session.add(Task(description='task1'))
    db.session.add(Task(description='task2'))
    db.session.add(Task(description='task3'))
    db.session.add(Task(description='task4'))
    db.session.add(Task(description='task5'))
    db.session.add(Task(description='task6'))

    
    db.session.commit()


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()

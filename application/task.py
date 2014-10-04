from celery.signals import task_postrun, worker_process_init
from application import celery, db
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from flask import current_app
from datetime import datetime
from application.twitter import TwitterFav


logger = get_task_logger(__name__)

@worker_process_init.connect
def celery_worker_init_db(**_):
    db.init_app(current_app)

@celery.task
def retweet(*recepients):
	logger.info("Start task")
	print "Retweeted"
	logger.info("Task finished: result")

@periodic_task(run_every=(crontab(minute='*/30')))
def favorite_tweet():
	logger.info("Start task")
	with current_app.app_context():
		tweet = TwitterFav()
		tweet.favoriteTweets()
	print "Tweet Favorited"
	logger.info("Task finished: result")

@task_postrun.connect
def close_session(*args, **kwargs):
	db.session.remove()
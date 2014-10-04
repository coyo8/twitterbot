from celery.signals import task_postrun, worker_process_init, task_prerun
from application import celery, db
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
from application.favoritetweet import TwitterFav


logger = get_task_logger(__name__)

@task_prerun.connect
def celery_prerun(*args, **kwargs):
	with celery.app.app_context():
		print db

@celery.task
def retweet(*recepients):
	logger.info("Start task")
	logger.info("Task finished: result")

@periodic_task(run_every=(crontab(minute='*/30')))
def favorite_tweet():
	logger.info("Start task")
	with celery.app.app_context():
		tweet = TwitterFav()
		tweet.favoriteTweets()
	logger.info("Task finished: result")

@task_postrun.connect
def close_session(*args, **kwargs):
	db.session.remove()
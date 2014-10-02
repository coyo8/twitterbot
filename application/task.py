from celery.signals import task_postrun
from application import celery, db
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime


logger = get_task_logger(__name__)


@celery.task
def retweet(*recepients):
	logger.info("Start task")
	print "Retweeted"
	logger.info("Task finished: result")

@periodic_task(run_every=(crontab(hour="*")))
def favorite_tweet():
	logger.info("Start task")
	print "Tweet Favorited"
	logger.info("Task finished: result")

@task_postrun.connect
def close_session(*args, **kwargs):
	db.session.remove()
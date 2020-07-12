from django.db import connection
from django.conf import settings

import twitter
import logging

logger = logging.getLogger(__name__)

def health_check_full():
    logger.debug('Performing full health check')
    return health_check_db() and health_check_twitter_api()

def health_check_db():
    logger.debug('Performing database health check')
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        if one != 1:
            logger.warn('Database health check failed')
            return False
    logger.debug('Database health check OK')
    return True

def health_check_twitter_api():
    logger.debug('Performing twitter API health check')
    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                    consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                    access_token_key=settings.TWITTER_APP_ACCESS_TOKEN,
                    access_token_secret=settings.TWITTER_ACCESS_SECRET)
    u = api.VerifyCredentials()
    if u != None:
        logger.debug('Twitter API health check OK')
        return True
    logger.warn('Twitter API health check failed')
    return False
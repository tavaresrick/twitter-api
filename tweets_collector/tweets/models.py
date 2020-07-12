from django.db import models, connection
from django.db.models import Max, Count
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime

import twitter
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class Tweet(models.Model):
    tag       = models.CharField(max_length=16)
    text      = models.CharField(max_length=280)
    date      = models.DateTimeField('date published')
    username  = models.CharField(max_length=50)
    language  = models.CharField(max_length=4,null=True)
    country   = models.CharField(max_length=128,null=True)
    followers = models.IntegerField(default=0)

class TweetManager():
    def populate():
        logger.info('Populating database')
        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                access_token_key=settings.TWITTER_APP_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_SECRET)
        logger.debug('Created Twitter API client')

        logger.debug('Clearing tweets table')
        Tweet.objects.all().delete()
        logger.debug('Tweets tabled cleared')

        for tag in settings.TWITTER_TAGS:
            logger.info('Fetching tweets with tag ' + tag)
            search_result = api.GetSearch(term=tag,
                count=100,
                result_type='recent')
            logger.debug('Tweets fetched with tag ' + tag)

            logger.debug('Creating tweets with tag ' + tag)
            for r in search_result:
                logger.debug(r)
                tweet = Tweet(
                    tag=tag,
                    text=r.text,
                    date=make_aware(datetime.strptime(r.created_at,'%a %b %d %H:%M:%S +0000 %Y')),
                    username=r.user.screen_name,
                    language=r.lang,
                    country=r.user.location,
                    followers=r.user.followers_count
                )
                tweet.save()
            logger.debug('Saved tweets with tag ' + tag)

        logger.info('Database populated')
        return True
        
    def top_users(total=5):
        logger.info('Getting top ' + str(total) + ' users')
        return Tweet.objects.values('username').annotate(Max('followers')).order_by('-followers__max')[:total]

    def by_hour():
        logger.info('Getting total tweets by hour')
        logger.debug('Getting database cursor')
        with connection.cursor() as cursor:
            logger.debug('Running database query to get total tweets by hour')
            cursor.execute("select to_timestamp(to_char(date, 'YYYY-MM-DD-HH24'), 'YYYY-MM-DD-HH24') date, count(1) total from tweets_tweet group by to_timestamp(to_char(date, 'YYYY-MM-DD-HH24'),'YYYY-MM-DD-HH24') order by 1")
            logger.debug('Executed database query to get total tweets by hour')
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
    
    def by_tag_country_language():
        logger.info('Getting total tweets by tag, country and language')
        return Tweet.objects.values('tag', 'country', 'language').annotate(Count('tag'))
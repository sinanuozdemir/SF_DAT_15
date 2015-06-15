import json
from database.models import Tweet, Tag, Person, Link, FacebookGroup, FacebookFanPage, FacebookPost, FacebookComment, FacebookLike, Topic, Importance, needsStats
from datetime import datetime, timedelta, date
import re
from django.db.models import Q, Count, Avg, Max, Min
import time
import json
import qsstats
import operator
from collections import defaultdict, Counter
import math
import numpy as np
from celery import shared_task
from celery.decorators import periodic_task
import Classifier
import networkx as nx
from textblob import TextBlob
from django.db import connection
from celery.schedules import crontab
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy import std, mean

def classifyText(text, topics = 'all'):
	text = text.strip().lower()
	topics_list = []
	if topics == 'all':
		topic_keywords = Topic.objects.exclude(keywords = None).values('pk', 'text', 'keywords')
	else:
		topic_keywords = Topic.objects.filter(text__in=topics).exclude(keywords = None).values('pk', 'text', 'keywords')
	for topic in topic_keywords:
		try:
			topic['keywords'] = json.loads(topic['keywords'])
		except:
			continue
		for keyword in topic['keywords']:
			if keyword.lower() in text:
				topics_list.append(topic['text'])
	return topics_list

@periodic_task(run_every=timedelta(hours=1))
def cleartaskmeta():
	cursor = connection.cursor()
	cursor.execute("truncate table celery_taskmeta")


def z_score(x, li):
	return float(x - mean(li))/std(li)

def tokenize(text):
	eturn text.split(' ')

def getImportantPhrases(recent, posts):
	week_ago = datetime.now() - timedelta(days=7)
	hour_ago = datetime.now() - timedelta(days=1)
	recent = Tweet.objects.filter(date__gte=hour_ago).values_list('text', flat=True)
	posts = Tweet.objects.filter(Q(date__lte=hour_ago)&Q(date__gte=week_ago)).values_list('text', flat=True)
	count_vect = CountVectorizer(tokenizer = tokenize, analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
	matrix =  count_vect.fit_transform(recent)
	len_posts = len(posts)
	len_recent = len(recent)
	freqs = [(word, matrix.getcol(idx).sum()) for word, idx in count_vect.vocabulary_.items()]
	top_ten = sorted (freqs, key = lambda x: -x[1])[:19]
	for word in top_ten:
		print word[0], float(word[1])/len_recent /  float(len([p for p in posts if word[0] in p.lower()])) / len_posts
		print "SDsdf"
		print (word[1] - sum([p for p in posts if word[0] in p.lower()]) / 48) / std([p for p in posts if word[0] in p.lower()])


def movingaverage(values,window):
	weigths = np.repeat(1.0, window)/window
	smas = np.convolve(values, weigths, 'valid')
	return smas # as a numpy array

def _frequency(num_tweets, days_in_between):
	rate = float(num_tweets) / days_in_between
	if rate < .5:
		return -4*(rate - .5)**2 + 1
	return 1. / (1+2.71828**(3*rate - 5))


@periodic_task(run_every=crontab(minute = '0', hour = '7'))
def getTwitterImportances(important_handles = []):
	important_handles = needsStats.objects.exclude(person=None).values_list('person__twitter_handle', flat = True)
	for handle in important_handles:
		try:
			handle = handle.lower().strip()
			getTwitterImportantPeopleFor(handle, days_ago = 1)
		except Exception as e:
			print e, "importance error"

@shared_task
def getTwitterImportantPeopleFor(twitter_handle = None, days_ago = 2, end_date = datetime.now()):
	important_person = Person.objects.get(twitter_handle=twitter_handle.lower().strip())
	start_date = end_date - timedelta(days=days_ago)
	days_in_between = int(round((end_date - start_date).total_seconds()/60./60/24))
	tweets_in_range = Tweet.objects.filter(Q(date__gte=start_date)&Q(date__lte=end_date)&Q(mentions__twitter_handle=twitter_handle.strip().lower()))
	counts = Counter(tweets_in_range.values_list('person__twitter_handle', flat=True))
	mentions = tweets_in_range.only('person').filter(Q(person__twitter_handle__in=counts.keys())).values('person__id', 'person__twitter_handle', 'mentions__twitter_handle','person__profile_image_url') 
	if len(mentions) == 0:
		return {}
	d = defaultdict(set)
	for mention in mentions:
		if mention['mentions__twitter_handle'] != None and mention['person__twitter_handle'] != None:
			d[mention['person__twitter_handle'].lower()].add(mention['mentions__twitter_handle'].lower())
	try:
		graph = nx.Graph(d)
		between = nx.betweenness_centrality(graph)
		eigen = nx.eigenvector_centrality_numpy(graph)
		frequencies = {f[0]: _frequency(f[1], days_in_between) for f in counts.iteritems()}
	except:
		return []
	longevity = {}
	images = {}
	total = []
	today = date.today()+timedelta(days=1)
	seven_days_ago = today - timedelta(days=7)
	seen = []
	for person in mentions:
		if person['person__twitter_handle'].lower() in seen:
			continue
		seen.append(person['person__twitter_handle'].lower())
		id_ = person['person__id']
		handle = person['person__twitter_handle']
		my_tweets = tweets_in_range.filter(Q(person__id=id_) & Q(date__gte=seven_days_ago) & Q(date__lte=today)).values('id')
		qss = qsstats.QuerySetStats(my_tweets, 'date')
		time_series = qss.time_series(seven_days_ago, today)
		li = [t[1] for t in time_series[:-1]]
		x = 6 - (x for x in reversed([y for y in enumerate(li)]) if x[1] == 0).next()[0] 
		longevity[handle] = .5*math.log(x + 1)
		images[handle] = person['person__profile_image_url']
	for handle in counts.keys():
		try:
			total.append( {'handle':handle,
								'importance': 
									round((2*frequencies[handle] + 2*longevity[handle] + 3*between[handle] + 3*eigen[handle])/10., 3),
								'image': images[handle]
								})
		except Exception as e:
			pass
	for t in total:
		try:
			i = Importance(person = Person.objects.get(twitter_handle=t['handle']), 
							in_regards_to = important_person,
							social_media = 'twitter',
							days_ago = days_ago,
							importance = t['importance']
						)
			i.save()
		except Exception as e:
			print "making importance error", e
	return sorted(total, key = lambda x: x['importance'], reverse = True)

def twitter_importance(tweets_in_range, days_in_between):
	counts = Counter(tweets_in_range.values_list('person__twitter_handle', flat=True))
	if len(counts.keys()) >= 10:
		counts = dict(sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
	mentions = tweets_in_range.only('person').filter(Q(person__twitter_handle__in=counts.keys())).values('person__id', 'person__twitter_handle', 'mentions__twitter_handle','person__profile_image_url') 
	if len(mentions) == 0:
		return {}
	d = defaultdict(set)
	for mention in mentions:
		if mention['mentions__twitter_handle'] != None and mention['person__twitter_handle'] != None:
			d[mention['person__twitter_handle'].lower()].add(mention['mentions__twitter_handle'].lower())
	graph = nx.Graph(d)
	between = nx.betweenness_centrality(graph)
	eigen = nx.eigenvector_centrality_numpy(graph)
	frequencies = {f[0]: _frequency(f[1], days_in_between) for f in counts.iteritems()}
	longevity = {}
	images = {}
	total = []
	today = date.today()+timedelta(days=1)
	seven_days_ago = today - timedelta(days=7)
	seen = []
	for person in mentions:
		if person['person__twitter_handle'].lower() in seen:
			continue
		seen.append(person['person__twitter_handle'].lower())
		id_ = person['person__id']
		handle = person['person__twitter_handle']
		my_tweets = tweets_in_range.filter(Q(person__id=id_) & Q(date__gte=seven_days_ago) & Q(date__lte=today)).values('id')
		qss = qsstats.QuerySetStats(my_tweets, 'date')
		time_series = qss.time_series(seven_days_ago, today)
		li = [t[1] for t in time_series[:-1]]
		x = 6 - (x for x in reversed([y for y in enumerate(li)]) if x[1] == 0).next()[0] 
		longevity[handle] = .5*math.log(x + 1)
		images[handle] = person['person__profile_image_url']
	for handle in counts.keys():
		try:
			total.append( {'handle':handle,
								'importance': 
									round((2*frequencies[handle] + 2*longevity[handle] + 3*between[handle] + 3*eigen[handle])/10., 3),
								'image': images[handle]
								})
		except Exception as e:
			print e
			pass
	return sorted(total, key = lambda x: x['importance'], reverse = True)

def _get_time_series(time_series, y_value, beginning_date, end_date, granularity = 'days', date_time = 'date'):
	qss = qsstats.QuerySetStats(time_series, date_time)
	if y_value == 'count':
		if granularity == 'days':
			time_series1 = qss.time_series(beginning_date, end_date, interval = granularity, aggregate=Count('id'))
			return [(datetime.strftime(t[0], '%D'), t[1]) for t in time_series1]
		else:
			granularity = int(granularity)
			time_series1 = qss.time_series(beginning_date, end_date, interval = 'minutes', aggregate=Count('id'))
			return zip([datetime.strftime(t[0], '%D %H:%M') for t in time_series1], movingaverage([t[1] for t in time_series1], granularity))
	elif y_value == 'sentiment':
		if granularity == 'days':
			time_series1 = qss.time_series(beginning_date, end_date, interval = granularity, aggregate=Avg('textblob_sentiment'))
			return [(datetime.strftime(t[0], '%D'), t[1]) for t in time_series1]
		else:
			granularity = int(granularity)
			time_series1 = qss.time_series(beginning_date, end_date, interval = 'minutes', aggregate=Avg('textblob_sentiment'))
			return zip([datetime.strftime(t[0], '%D %H:%M') for t in time_series1], movingaverage([t[1] for t in time_series1], granularity))
	else:
		return []
	return []

@shared_task
def ego_frequency(beginning_date, end_date, handles = [], fbs = [], tags = [], days_ago = 7, topics = ['any'], y_value='count', granularity = 'days'):
	topic_q =  reduce(operator.or_, [Q(topics__text__iexact = topic) for topic in topics])
	to_return = {}
	if len(handles+tags) and (handles[0] or tags[0]):
		twitter_query = (Q(date__gte=beginning_date) & Q(date__lte=end_date))
		if handles and handles[0]:
			twitter_query &= reduce(operator.or_, [Q(mentions__twitter_handle__iexact=handle) for handle in handles])
		elif tags and tags[0]:
			twitter_query &= reduce(operator.or_, [Q(tags__text__iexact="#"+tag) for tag in tags])
		if topics != ['any']:
			twitter_query &= topic_q
		tweets =  Tweet.objects.filter(twitter_query)
		to_return['tweets'] = _get_time_series(tweets, y_value, beginning_date, end_date, granularity = granularity)
		try:
			people =  list(Importance.objects.filter(Q(in_regards_to__twitter_handle__in = handles) & Q(date_created__gte=datetime.now() - timedelta(days=days_ago))).values('date_created', 'person', 'in_regards_to').order_by('person', '-date_created').distinct('person').values('person__twitter_handle', 'person__name', 'person__profile_image_url', 'importance'))
			to_return['twitter_importance'] = people
		except Exception as e:
			to_return['twitter_importance'] = []
	if len(fbs) and fbs[0]:
		fb_post_q = (Q(date_posted__gte=beginning_date) & Q(date_posted__lte=end_date))&reduce(operator.or_, [Q(fan_page__page_id__iexact=facebook_id) for facebook_id in fbs])
		fb_comment_q = (Q(date_commented__gte=beginning_date) & Q(date_commented__lte=end_date))&reduce(operator.or_, [Q(post__fan_page__page_id__iexact=facebook_id) for facebook_id in fbs])
		comments = FacebookComment.objects.filter(fb_comment_q)
		posts = FacebookPost.objects.filter(fb_post_q)
		if topics != ['any']:
			fb_comment_q &= topic_q
			fb_post_q &= topic_q
		try:
			people =  list(Importance.objects.filter(Q(fb_fan_page_regards_to__page_id__in = fbs) & Q(date_created__gte=datetime.now() - timedelta(days=days_ago))).values('date_created', 'person', 'in_regards_to').order_by('person', '-date_created').distinct('person').values('person__facebook_id', 'person__name', 'person__profile_image_url', 'importance'))
			to_return['facebook_importance'] = people
		except Exception as e:
			to_return['facebook_importance'] = []
		commentt = _get_time_series(comments.values('textblob_sentiment', 'id'), y_value, beginning_date, end_date, date_time = 'date_commented', granularity = granularity)
		postt = _get_time_series(posts.values('textblob_sentiment', 'id'), y_value, beginning_date, end_date, date_time = 'date_posted', granularity = granularity)
		to_return['facebook_comments'] = commentt
		to_return['facebook_posts'] = postt
	return to_return

@periodic_task(run_every=crontab(minute = '0', hour = '7'))
def getFacebookImportances(important_facebook_ids = []):
	important_facebook_ids = needsStats.objects.exclude(facebook_fan_page = None).values_list('facebook_fan_page__page_id', flat = True)
	for fb in important_facebook_ids:
		try:
			fb = fb.lower().strip()
			getFacebookImportantPeopleFor(fb, days_ago = 1)
		except Exception as e:
			print e, "importance error"

@shared_task
def getFacebookImportantPeopleFor(facebook_id = None, days_ago = 2, end_date = datetime.now()):
	important_person = FacebookFanPage.objects.get(page_id=facebook_id)
	start_date = end_date - timedelta(hours=24*days_ago)
	fb_post_q = reduce(operator.or_, [Q(fan_page__page_id__iexact=facebook_id)])&Q(date_posted__gte=start_date)&Q(date_posted__lte=end_date)
	fb_comment_q = reduce(operator.or_, [Q(post__fan_page__page_id__iexact=facebook_id)])&Q(date_commented__gte=start_date)&Q(date_commented__lte=end_date)
	posts = FacebookPost.objects.filter(fb_post_q)
	comments = FacebookComment.objects.filter(fb_comment_q)
	likes = FacebookLike.objects.filter(Q(post__in=posts) | Q(comment__in=comments)).values('author__facebook_id', 'post__author__facebook_id', 'comment__author__facebook_id')
	comments = Counter(comments.values_list('author__facebook_id', flat = True))
	people = defaultdict(set)
	for like in likes:
		if like['comment__author__facebook_id']:
			people[like['author__facebook_id']].add(like['comment__author__facebook_id'])
		else:
			people[like['author__facebook_id']].add(like['post__author__facebook_id'])
	graph = nx.Graph(people)
	between = nx.betweenness_centrality(graph)
	total = {}
	for fb_person_id in people:
		total[fb_person_id] = (3 * between[fb_person_id] + 2 * comments.get(fb_person_id, 0) +  2 * len(people[fb_person_id])) / 7
	for t in total:
		try:
			i = Importance(person = Person.objects.get(facebook_id=t), 
							fb_fan_page_regards_to = important_person,
							social_media = 'facebook',
							days_ago = days_ago,
							importance = total[t]
						)
			i.save()
		except Exception as e:
			print "making facebook importance error", e
		print t
	

'''
INPUT: facebook_person_dict -> raw json format of a person from facebook
OUTPUT: person -> model of a Person
        p_created -> True if the person was created, False otherwise (if they already existed)
'''
@shared_task
def makePersonFacebook(facebook_person_dict):
	new_dict = {}
	unique_ = {}
	for old_key, new_key in [('id', 'facebook_id'), ('name', 'name')]:
		if facebook_person_dict.get(old_key, None):
			try:
				new_dict[new_key] = facebook_person_dict[old_key].lower()
			except:
				new_dict[new_key] = facebook_person_dict[old_key]
			if old_key in ['id', 'facebook_id']:
				unique_[new_key] = facebook_person_dict[old_key].lower()
	q = reduce(operator.or_, [Q(**{k: v}) for k, v in unique_.iteritems()])
	people = Person.objects.filter(q)
	if not len(people):
		p = Person(**new_dict)
		try:
			p.profile_image_url = facebook_person_dict.get('picture', {}).get('url', '')
		except Exception as e:
			print e, "facebook image error"
		p.save()
		return p, True
	person = people[0]
	return person, False

@shared_task
def makeFacebookGroup(facebook_group_dict):
	return FacebookGroup.objects.get_or_create(group_id = facebook_group_dict['gid'], defaults = {'name':facebook_group_dict['name']})

@shared_task
def makeFacebookFanPage(facebook_fan_dict):
	return FacebookFanPage.objects.get_or_create(page_id = facebook_fan_dict['page_id'], defaults = {'name':facebook_fan_dict['name']})

@shared_task
def makeFacebookLike(facebook_like_dict):
	person_id = facebook_like_dict['id']
	person, person_created = Person.objects.get_or_create(facebook_id = person_id)
	try:
		if 'comment_id' in facebook_like_dict.keys():
			comment = FacebookComment.objects.get_or_create(comment_id = facebook_like_dict['comment_id'])[0]
			return FacebookLike.objects.get_or_create(comment = comment, author = person)
		elif 'post_id' in facebook_like_dict.keys():
			post = FacebookPost.objects.get_or_create(post_id = facebook_like_dict['post_id'])[0]
			return FacebookLike.objects.get_or_create(post = post, author = person)
	except Exception as e:
		print e, "facebook like error"
	return None, None

@shared_task
def makeFacebookPost(facebook_post_dict, topics = False, sentiment = False):
	post, post_created = FacebookPost.objects.get_or_create(post_id = facebook_post_dict['id'])
	author, author_created = Person.objects.get_or_create(facebook_id = facebook_post_dict['from']['id'], defaults={'name': facebook_post_dict['from'].get('name', '')})
	post.author = author
	post.text = facebook_post_dict.get('message', '')
	post.date_posted = datetime.strptime(facebook_post_dict['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
	post.save()
	post.fan_page = FacebookFanPage.objects.get_or_create(page_id=facebook_post_dict.get('object_id',1))[0]
	if topics:
		c = Classifier.classifier()
		post.topics.add(*[Topic.objects.get_or_create(text=topi)[0] for topi in c.get_topics_for(facebook_post_dict['message'])])
	if sentiment:
		post.textblob_sentiment = TextBlob(facebook_post_dict['message']).sentiment.polarity
	post.save()
	return post, post_created

@shared_task
def makeFacebookComment(facebook_comment_dict, topics = False, sentiment = False):
	comment, comment_created = FacebookComment.objects.get_or_create(comment_id = facebook_comment_dict['id'])
	if not comment_created:
		return comment, comment_created
	author, author_created = Person.objects.get_or_create(facebook_id = facebook_comment_dict['from']['id'], defaults={'name': facebook_comment_dict['from'].get('name', '')})
	comment.author = author
	comment.text = facebook_comment_dict.get('message', '')
	comment.save()
	comment.date_commented = datetime.strptime(facebook_comment_dict['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
	if 'post_id' in facebook_comment_dict.keys():
		comment.post = FacebookPost.objects.get_or_create(post_id = facebook_comment_dict['post_id'])[0]
	elif 'comment_id' in facebook_comment_dict.keys():
		comment.parent = FacebookComment.objects.get_or_create(comment_id = facebook_comment_dict['comment_id'])[0]
	if topics:
		c = Classifier.classifier()
		comment.topics.add(*[Topic.objects.get_or_create(text=topi)[0] for topi in c.get_topics_for(facebook_comment_dict['message'])])
	if sentiment:
		comment.textblob_sentiment = TextBlob(facebook_comment_dict['message']).sentiment.polarity
	comment.save()
	return comment, comment_created

def storeTweet(tweet_dict):
	t, created = Tweet.objects.get_or_create(status_id = tweet_dict['id_str'])
	if created:
		try:
			t.rawJSON = json.dumps(tweet_dict)
			t.text = tweet_dict['text']
			t.save()
		except Exception as e:
			print "Storing error", e
	return t, created

@shared_task
def fullMakeTweet(tweet_dict, topics = False, sentiment = False):
	try:
		t, created = Tweet.objects.get_or_create(status_id = tweet_dict['id_str'])
	except Exception as e:
		return None, e
	if not created:
		return t, False
	t.text = tweet_dict['text']
	t.save()
	try:
		t.tags.add(*[Tag.objects.get_or_create(text = tag.lower())[0] for tag in re.findall("([\$|\#]\w+)", tweet_dict['text'])])
	except:
		pass
	try:
		t.mentions.add(*[Person.objects.get_or_create(twitter_handle=mention[1:].lower())[0] for mention in re.findall("(@\w*)", tweet_dict['text']) if len(mention) >= 2])
	except:
		pass
	t.person = makePersonTwitter(tweet_dict['user'])[0]
	t.date = datetime.strptime(tweet_dict['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
	t.save()
	if topics:
		# c = Classifier.classifier()
		# t.topics.add(*[Topic.objects.get_or_create(text=topi)[0] for topi in c.get_topics_for(tweet_dict['text'])])
		t.topics.add(*[Topic.objects.get_or_create(text=topi)[0] for topi in classifyText(tweet_dict['text'])])
	if sentiment:
		t.textblob_sentiment = TextBlob(tweet_dict['text']).sentiment.polarity
	if 'retweeted_status' in tweet_dict.keys():
		t.retweet = tweet_dict['retweeted_status']['id_str']
	t.save()
	return t, True

# get topics, sentiment, etc
@shared_task
def analyzeTweet(tweet_id):
	t, created = Tweet.objects.get_or_create(status_id = tweet_id)
	tweet_text = t.text
	c = Classifier.classifier()
	topics = c.get_topics_for(tweet_text)
	for topic in topics:
		if topic is None:
			continue
		topic_, created = Topic.objects.get_or_create(text=topic)
		topic_.save()
		t.topics.add(topic_)
	try:
		blob = TextBlob(tweet_text)
		sent =  blob.sentiment.polarity
	except:
		sent = 0
	t.textblob_sentiment = sent
	t.save()
	return {'sentiment':sent, 'text':tweet_text, 'topics':topics}

# Assumes id_str is in the dictionary
# also assumes that person's id's are unique
def newMakePersonTwitter(twitter_person_dict):
	if 'id_str' not in twitter_person_dict.keys():
		return None, None
	new_dict = {}
	for old_key, new_key in [('profile_image_url', 'profile_image_url'), ('id_str', 'twitter_id'), ('screen_name', 'twitter_handle'), ('name', 'name'), ('followers_count', 'twitter_followers'), ('friends_count', 'twitter_following'), ('description', 'twitter_desc')]:
		new_dict[new_key] = twitter_person_dict.get(old_key, '')
	p, p_created = Person.objects.get_or_create(twitter_id = twitter_person_dict['id_str'], defaults = new_dict)
	return p, p_created

'''
INPUT: twitter_person_dict -> raw json format of a person
OUTPUT: person -> model of a Person
        p_created -> True if the person was created, False otherwise (if they already existed)
'''
@shared_task
def makePersonTwitter(twitter_person_dict):
	new_dict = {}
	unique_ = {}
	for old_key, new_key in [('profile_image_url', 'profile_image_url'), ('id_str', 'twitter_id'), ('screen_name', 'twitter_handle'), ('name', 'name'), ('followers_count', 'twitter_followers'), ('friends_count', 'twitter_following'), ('description', 'twitter_desc')]:
		if twitter_person_dict.get(old_key, None):
			try:
				new_dict[new_key] = twitter_person_dict[old_key].lower()
			except:
				new_dict[new_key] = twitter_person_dict[old_key]
			if old_key in ['id_str', 'screen_name']:
				unique_[new_key] = twitter_person_dict[old_key].lower()
	q = reduce(operator.or_, [Q(**{k: v}) for k, v in unique_.iteritems()])
	people = Person.objects.filter(q)
	if not len(people):
		p = Person(**new_dict)
		p.save()
		return p, True
	person = people[0]
	if not person.twitter_id:
		Person.objects.filter(id=person.id).update(**new_dict)
	return person, False



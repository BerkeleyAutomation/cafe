#!/usr/bin/env python
#coding=utf-8
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *
import json
from django.db.models import Q
from django.db.models import *
from django.contrib.auth.models import User
import goslate

googleTranslate = goslate.Goslate()

def translateToEnglish(comment):
    return "english(" + comment + ")"

def translateToSpanish(comment):
    return googleTranslate.translate(comment,'es')

for comment in DiscussionComment.objects.all():
# 	if not comment.is_current and comment.original_language = 'spanish':
# 		is_current = datetime.datetime.now()
# 		comment.comment = translateToEnglish(comment.spanish_comment)
# 	if not comment.is_current and comment.original_language = 'english':
# 		is_spanish_current = datetime.datetime.now()
# 		comment.comment = translateToSpanish(comment.comment)
# 	comment.save()
	print(comment.comment)
	print
	print
	print
	print

	try:
		spanComment = translateToSpanish(comment.comment)
	except BaseException:
		print("there was an error in translating: " + comment.comment)
		print
		print
		print
		print
	
	if len(spanComment) > 1024:
		comment.spanish_comment = spanComment[0:1023]
	else:
		comment.spanish_comment = spanComment

	print(comment.spanish_comment)
	print
	print
	print
	print
	comment.save()

# for comment in DiscussionComment.objects.all():
# 	if(comment.comment.startswith("California is economically in the toilet.")):
# 		print(len(comment.comment))
# 		print(len(translateToSpanish(comment.comment)))
# 		print(translateToSpanish(comment.comment)[0:1023])


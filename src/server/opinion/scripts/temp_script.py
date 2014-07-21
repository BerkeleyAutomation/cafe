#!/usr/bin/env python
#coding=utf-8
import environ
from opinion.opinion_core.models import *
from opinion.opinion_core.modelsMulti import *
import numpy as np
from opinion.includes.queryutils import *
import json
from django.db.models import Q
from django.db.models import *
from django.contrib.auth.models import User

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1
print json.dumps(counties)
"""
"""
geo_json=open('../geo-ca.json')
geo_data=json.load(geo_json)
counties = {}
for i in range(0,len(geo_data['features'])):
    county=geo_data['features'][i]['properties']['NAME']
    zipcode_in_county=ZipCode.objects.filter(state='CA').filter(county__startswith=county)
    if len(zipcode_in_county) > 0:
        counties[county] = ZipCodeLog.objects.filter(location__in=zipcode_in_county).count()/(geo_data['features'][i]['properties']['Population']/10000.0)
print json.dumps(counties)
"""

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1

counties2 = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0 and CommentAgreement.objects.filter(is_current=True,rater=u).count() > 5:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties2:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
        else:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
print json.dumps(counties2)
"""

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0 and UserRating.objects.filter(is_current=True, user = u).count() > 3:
        m = np.mean(UserRating.objects.filter(is_current=True, user = u).values_list('rating'))
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]].append(m)
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = [m]

counties2 = {}
for c in counties:
    counties2[c] = 1-np.median(counties[c])
print json.dumps(counties2)

"""
"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1

counties2 = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    comment = ""
    if DiscussionComment.objects.filter(user = u,is_current=True).count() > 0:
        c = DiscussionComment.objects.filter(user = u,is_current=True)[0]
        tag_object = AdminCommentTag.objects.filter(comment = c)
        if tag_object.count() > 0:
            comment = tag_object[0].tag.lower()

    if len(zc_log_object) > 0 and (('disaster' in comment)):
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties2:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
        else:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
print json.dumps(counties2)
"""


"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    comments = AdminCommentTag.objects.filter(Q(tag__icontains="disaster")).values("comment")
    if len(zc_log_object) > 0 and CommentAgreement.objects.filter(is_current=True, rater = u, comment__in = comments).count() > 0:
        m = np.mean(CommentRating.objects.filter(is_current=True, rater = u, comment__in = comments).values_list('rating'))
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]].append(m)
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = [m]

counties2 = {}
for c in counties:
    counties2[c] = 1-np.median(counties[c])
print json.dumps(counties2)
"""
"""
for r in CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(Q(is_current=True, comment__icontains='water', user__in=User.objects.filter(is_active=True))), is_current=True).order_by('created'):
    if r.agreement != .5:
        print 1-r.agreement
"""


# state = OpinionSpaceStatement.objects.get(statement_number=0)
# state.statement = "La aplicacion de la Ley de Asistencia Asequible ('Obamacare')"
# print(state.statement)
# # state.short_version = "slider"
# state.save()




# state = OpinionSpaceStatement.objects.get(statement_number=1)
# state.statement = "Calidad de la educacion K-12 publicas"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=2)
# state.statement = "Asequibilidad de los colegios y universidades estatales"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=3)
# state.statement = "El acceso a los servicios estatales para los inmigrantes indocumentados"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=4)
# state.statement = "Leyes y reglamentos relativos a la marihuana recreativa"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=5)
# state.statement = "Los derechos de matrimonio para parejas del mismo sexo"
# print(state.statement)
# # state.short_version = "slider"
# state.save()

# class Place(Model):
#     name = CharField(max_length=50)
#     address = CharField(max_length=80)

#     def __str__(self):              # __unicode__ on Python 2
#         return "%s the place" % self.name

# class Restaurant(Model):
#     place = OneToOneField(Place, primary_key=True)
#     serves_hot_dogs = BooleanField()
#     serves_pizza = BooleanField()

#     def __str__(self):              # __unicode__ on Python 2
#         return "%s the restaurant" % self.place.name

def translate(comment):
    # validatedComment = validate(comment)
    # return validatedComment
    return "spanish(" + comment + ")"

# firstComment = DiscussionComment.objects.get(id=1)
# firstComment.spanish_comment = "California tiene una de las politicas ambientales mas progresistas de la nacion, debemos trabajar mas para hacer de California un centro internacional de 'tecnologia verde'. Esta inversion equilibra valores de la innovacion y la responsabilidad ambiental de nuestro estado."
# firstComment.original_language = "english"
# firstComment.save()

#firstComment = DiscussionComment.objects.get(id=1)
# print(firstComment.spanish_comment)
# print(firstComment.original_language)


# state = OpinionSpaceStatement.objects.get(statement_number=0)
# state.statement = 'Implementation of the Affordable Care Act ("Obamacare")'
# state.spanish_statement = u"La aplicación de la Ley de Asistencia Asequible ('Obamacare')"
# print(state.statement)
# print(state.spanish_statement)
# state.input_type = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=1)
# state.statement = 'Quality of K-12 public education'
# state.spanish_statement = u"Calidad de la educación K-12 públicas"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=2)
# state.statement = 'Affordability of state colleges and universities'
# state.spanish_statement = u"Asequibilidad de los colegios y universidades estatales"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=3)
# state.statement = 'Access to state services for undocumented immigrants'
# state.spanish_statement = u"El acceso a los servicios estatales para los inmigrantes indocumentados"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=4)
# state.statement = 'Laws and regulations regarding recreational marijuana'
# state.spanish_statement = u"Leyes y reglamentos relativos a la marihuana recreativa"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# state = OpinionSpaceStatement.objects.get(statement_number=5)
# state.statement = 'Marriage rights for same-sex partners'
# state.spanish_statement = u"Los derechos de matrimonio para parejas del mismo sexo"
# print(state.statement)
# print(state.spanish_statement)
# # state.short_version = "slider"
# state.save()

# super_user = User.objects.get(pk=1)
# print(super_user.username)
# super_user.set_password("crc")
# super_user.save()

for comment in DiscussionComment.objects.all():
    comment.spanish_comment = translate(comment.comment)
    print(comment.spanish_comment)
    comment.save()


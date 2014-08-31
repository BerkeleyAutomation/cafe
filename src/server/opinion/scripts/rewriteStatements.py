# -*- coding: utf-8 -*-
#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *
import json
from django.db.models import Q

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


opinionSpaceObject = OpinionSpace.objects.filter(id=1)[0]

def createOpinionSpaceStatement(stateNum,className, state=''):
    
    prevStatements = OpinionSpaceStatement.objects.filter(statement_number=stateNum)
    if len(prevStatements) != 0:
        print("Statement:" + prevStatements[0].statement + "\n already exists. Another one cannot be created without deleting existing statement")
    else:
        newStatement = OpinionSpaceStatement(statement_number=stateNum, statement=state, short_version=className, opinion_space=opinionSpaceObject)
        newStatement.opinion_space = opinionSpaceObject
        newStatementMedian = StatementMedians(rating=0.5)
        newStatementMedian.statement = newStatement
        newStatement.save()
        newStatementMedian.save()

def deleteOpinionSpaceStatement(stateNum):
    state = OpinionSpaceStatement.objects.filter(statement_number=stateNum)
    if len(state) == 0:
        print("No Statement to Delete! No statement asseociated with id num:" + str(stateNum))
        return
    stateMed = StatementMedians.objects.all()
    for item in stateMed:
        if (item.statement==state[0]):
            item.delete()
    for item in state:
        state.delete()


state = OpinionSpaceStatement.objects.get(statement_number=0)
state.spanish_statement = u"Aplicación de la Ley de Cuidado de Salud Asequible ('Obamacare')"
state.short_version = "slider"
state.save()

state = OpinionSpaceStatement.objects.get(statement_number=1)
state.spanish_statement = "Calidad de la educación pública K-12"
state.short_version = "slider"
state.save()

state = OpinionSpaceStatement.objects.get(statement_number=2)
state.spanish_statement = "Asequibilidad de los colleges y universidades estatales"
state.short_version = "slider"
state.save()

state = OpinionSpaceStatement.objects.get(statement_number=3)
state.spanish_statement = "Acceso de inmigrantes indocumentados a servicios estatales"
state.short_version = "slider"
state.save()

state = OpinionSpaceStatement.objects.get(statement_number=4)
state.spanish_statement = "Leyes y regulaciones con respecto al uso recreativo de la mariguana"
state.short_version = "slider"
state.save()

state = OpinionSpaceStatement.objects.get(statement_number=5)
state.spanish_statement = "Derecho al matrimonio para parejas del mismo sexo"
state.save()


# for num in range(5,12):
#     deleteOpinionSpaceStatement(num)

# Knowledge
# createOpinionSpaceStatement(stateNum=5, className="slider", state="Implementation")
#deleteOpinionSpaceStatement(1)
# createOpinionSpaceStatement(1, "slider", state="Aplicacion del Affordable Care Act (ObamaCare)")
# createOpinionSpaceStatement(7, "slider", state="What is the percent likelihood that an earthquake of 7.5 magnitude or larger will occur in Southern California in the next 30 years?")


# Preparedness
# createOpinionSpaceStatement(6, "slider", state="If I had to evacuate my building immediately and did not have a working cell-phone, members of my household would know where to meet.")
# createOpinionSpaceStatement(9, "slider", state="If I had to evacuate my neighborhood immediately and did not have a working cell-phone, members of my household would know where to meet.")
# createOpinionSpaceStatement(10, "slider", state="If I had to fully evacuate my city, members of my household would all know where to go.")
# createOpinionSpaceStatement(11, "slider", state="How many of the following items do you have in your house?")

# state = OpinionSpaceStatement.objects.get(statement_number=5)
# state.statement = "How many miles from a major faultline is your household?"
# state.short_version = "slider"
# state.save()


# for land in OpinionSpaceStatement.objects.all():
#     print(land)
#     print(land.statement_number)
#     print(land.statement)
#     print(land.short_version)
#     print(land.created)

for median in StatementMedians.objects.all():
    print(median.rating)
    print(median.statement)

# for statement in statements:
#     print(statement)
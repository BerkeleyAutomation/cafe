from django.http import HttpResponse
from django.core.urlresolvers import reverse

from opinion.opinion_core.models import *

import twilio.twiml
import random

statement_text = [
    "implementation of the Affordable Care Act, also known as Obamacare",
    "quality of K through 12 public education",
    "affordability of state colleges and universities",
    "access to state services for undocumented immigrants",
    "laws and regulations regarding recreational marijuana",
    "marriage rights for same-sex partners",
]

def get_comment():
    all_comments = DiscussionComment.objects.filter(is_current=True, blacklisted=False)
    return random.choice(all_comments).comment

def begin(request):
    resp = twilio.twiml.Response()

    resp.say("Welcome to the California Report Card, a project by the "
             "Connected Communities Initiative at UC Berkeley, "
             "and the Office of Lieutenant Governor Gavin Newsom.")
    resp.pause(length=1)
    resp.say("By filling out the report card, you can join twenty thousand "
             "other Californians to help identify top priorities for "
             "the California State Budget")

    resp.redirect(reverse(statement, args=[0]))
    return HttpResponse(str(resp))

def statement(request, num):
    resp = twilio.twiml.Response()
    num = int(num)

    resp.pause(length=1)
    if num == 0:
        resp.say("To submit your grades, press the number keys on your phone. "
                 "0 is the lowest possible grade, and 9 is the highest grade. ")
        resp.pause(length=1)
    else:
        pass
        # TODO: save Digits param for previous rating

    if num == OpinionSpaceStatement.objects.filter().count():
        resp.redirect(reverse(demographic))
    else:
        intros = ["First", "Next", "Now", "", "", "Finally"]

        # statement_text = list(OpinionSpaceStatement.objects.all())[num].statement
        with resp.gather(numDigits=1, action=reverse(statement, args=[num+1]),
                         finishOnKey="any digit", timeout=60) as g:
            ask_grade = "{}, grade the state {} on the {}.".format(
                intros[num],
                'of California' if num <= 2 else '',
                statement_text[num],
            )
            g.say(ask_grade)

    return HttpResponse(str(resp))

def demographic(request):
    resp = twilio.twiml.Response()
    with resp.gather(numDigits=5, action=reverse(peer_rate, args=[0]),
                     finishOnKey="any digit", timeout=60) as g:
            g.say("Would you like to join a discussion on what issue "
                  "should be included on the next California Report Card")
            g.pause(length=2)
            g.say("Enter your zip code to continue.")
    return HttpResponse(str(resp))

def peer_rate(request, num):
    resp = twilio.twiml.Response()
    num = int(num)

    if num == 0:
        resp.say("Before you tell us what you think should be included in "
                 "the next report card, please rate suggestions from "
                 "two other participants....")
        with resp.gather(numDigits=1, action=reverse(peer_rate, args=[num+1]),
                         finishOnKey="any digit", timeout=60) as g:
            g.say("Rate this idea...")
            g.pause(length=2)
            g.say(get_comment())
    else:
        # TODO: save Digits param for previous rating
        pass

    if num == 1:
        resp.say("You're halfway there! Just rate one more suggestion "
                 "and then you can tell us yours")
        with resp.gather(numDigits=1, action=reverse(peer_rate, args=[num+1]),
                         finishOnKey="any digit", timeout=60) as g:
            g.say("The suggestion is...")
            g.pause(length=2)
            g.say(get_comment())

    if num >= 2:
        resp.redirect(reverse(record_comment))

    return HttpResponse(str(resp))

def record_comment(request):
    resp = twilio.twiml.Response()
    resp.say("Now, record your suggestion for the next report card after "
             "the tone. Press any key when you're finished.")
    resp.pause(length=2)
    resp.record(action=reverse(finish), timeout=15)
    return HttpResponse(str(resp))

def finish(request):
    # TODO: save Recording param for previous rating
    resp = twilio.twiml.Response()
    resp.say("Thank you for completing the California Report Card. Please "
             "share this telephone number with other Californians "
             "and call back at anytime to re-grade the state. Good bye!")
    return HttpResponse(str(resp))


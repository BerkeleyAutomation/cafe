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

def url(fname):
    return "http://californiareportcard.org/uganda2/media/audio/" + fname

def get_comment():
    all_comments = DiscussionComment.objects.filter(is_current=True, blacklisted=False)
    return random.choice(all_comments)

def begin(request):
    resp = twilio.twiml.Response()

    resp.say("Welcome to the reproductive health survey", voice='alice')
    resp.pause(length=1)

    resp.redirect(reverse(statement, args=[0]))
    return HttpResponse(str(resp))

def statement(request, num):
    resp = twilio.twiml.Response()
    num = int(num)

    resp.pause(length=1)
    if num == 0:
        resp.play(url("listen-statement-instructions.wav"))
        resp.pause(length=1)
    else:
        pass
        # TODO: save Digits param for previous rating

    if num == OpinionSpaceStatement.objects.filter().count():
        # resp.redirect(reverse(demographic))
        resp.redirect(reverse(peer_rate, args=[0]))
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
            # g.say(ask_grade)
            g.play(url('statement-{}.wav'.format(num+1)))

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
        resp.play(url('leaves-instructions.wav'))
        with resp.gather(numDigits=1, action=reverse(peer_rate, args=[num+1]),
                         finishOnKey="any digit", timeout=60) as g:
            g.say("Rate this idea...", voice='alice')
            g.pause(length=2)
            g.play(url('{}.wav').format(get_comment().id))
    else:
        # TODO: save Digits param for previous rating
        pass

    if num == 1:
        resp.say("Just rate one more suggestion and then you can tell us yours", voice='alice')
        with resp.gather(numDigits=1, action=reverse(peer_rate, args=[num+1]),
                         finishOnKey="any digit", timeout=60) as g:
            g.say("The suggestion is...", voice='alice')
            g.pause(length=2)
            g.play(url('{}.wav').format(get_comment().id))

    if num >= 2:
        resp.redirect(reverse(record_comment))

    return HttpResponse(str(resp))

def record_comment(request):
    resp = twilio.twiml.Response()
    resp.say("Now, record your suggestion after the tone. Press any key when you're finished.", voice='alice')
    resp.pause(length=2)
    resp.record(action=reverse(finish), timeout=15)
    return HttpResponse(str(resp))

def finish(request):
    # TODO: save Recording param for previous rating
    resp = twilio.twiml.Response()
    resp.say("Thank you for completing the reproductive health survey. Please "
             "encourage other women to take this survey too. Good bye! ", voice='alice')
    return HttpResponse(str(resp))


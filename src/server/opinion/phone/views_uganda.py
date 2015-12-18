from django.http import HttpResponse
from django.core.urlresolvers import reverse

from opinion.includes.logutils import *
from opinion.opinion_core.models import *

import twilio.twiml
import random
import os

# statement_text = [
#     "implementation of the Affordable Care Act, also known as Obamacare",
#     "quality of K through 12 public education",
#     "affordability of state colleges and universities",
#     "access to state services for undocumented immigrants",
#     "laws and regulations regarding recreational marijuana",
#     "marriage rights for same-sex partners",
# ]
DEBUG = os.environ.get('DEVCAFEDEBUG', False)
SHORT = os.environ.get('DEVCAFESHORT', False)

def url(fname):
    if DEBUG:
        return "http://cafe.ngrok.com/media/audio/" + fname
    return "http://californiareportcard.org/uganda2/media/audio/" + fname

def get_comment():
    """Returns (cid, url)"""
    all_comments = list(DiscussionComment.objects.filter(is_current=True, blacklisted=False))
    random.shuffle(all_comments)
    c = all_comments[0]

    if 'twilio' in c.comment:
        return c.id, c.comment
    return c.id, url(str(c.id) + ".mp3")

def find_username_from_CallSid (callSID): #TODO: add error handling
    # print callSID
    # truncated_callSid = callSID[:15]
    # username = 'p' + truncated_callSid + '@example.com'
    # return username
    return callSID

def begin(request):
    callsid = request.POST.get("CallSid")
    if callsid:
        username = find_username_from_CallSid(callsid)
        random_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        user = User.objects.create_user(username=username, password=random_password)
        user.save()

    resp = twilio.twiml.Response()

    # resp.say("Welcome to the reproductive health survey", voice='alice')
    resp.play(url("inst1.mp3"))
    resp.pause(length=1)

    # resp.play(url("inst2.mp3"))
    # resp.pause(length=1)

    resp.play(url("inst3.mp3"))
    resp.pause(length=1)
    resp.record(action=reverse(save_edu_center), timeout=10, maxLength=10)
    return HttpResponse(str(resp))

def save_edu_center(request):
    resp = twilio.twiml.Response()
    audio_recording = request.POST.get('RecordingUrl', "")
    username = find_username_from_CallSid(request.POST.get("CallSid", ""))
    user = User.objects.get(username = username)
    ud = UserData(user=user, key="edu_center", value=audio_recording)
    ud.save()
    resp.redirect(reverse(statement, args=[0]))
    return HttpResponse(str(resp))

def statement(request, num):
    resp = twilio.twiml.Response()
    num = int(num)

    resp.pause(length=1)

    if (num == 0) and (not SHORT) :
        resp.play(url("inst4.mp3"))
        # resp.play(url("listen-statement-instructions.wav"))
        resp.pause(length=1)
    else:
        username = find_username_from_CallSid(request.POST.get("CallSid", ""))
        user = User.objects.get(username = username)

        rating = request.POST.get("Digits", "")
        # attempt to cast to an int?
        num_rating = -1
        try:
            num_rating = int(rating)
        except ValueError:
            pass
        # value = -1
        # if (num_rating < 0 or num_rating > 4): # not a valid rating
        #     pass # Repeat the instructions
        # else:
        # value = num_rating / 5.0
        # TODO: save Digits param for previous rating
        rating = UserRating(user = user,
                    opinion_space_id = 1, # Is this okay?
                    opinion_space_statement = OpinionSpaceStatement.objects.get(pk=num),
                    rating = num_rating,
                    is_current = True)
        rating.save()

    thresh = 2 if SHORT else OpinionSpaceStatement.objects.filter().count()
    if num == thresh:
        # resp.redirect(reverse(demographic))
        resp.redirect(reverse(peer_rate, args=[0, 0]))
        return HttpResponse(str(resp))

    # intros = ["First", "Next", "Now", "", "", "Finally"]

    # statement_text = list(OpinionSpaceStatement.objects.all())[num].statement
    with resp.gather(numDigits=1, action=reverse(statement, args=[num+1]),
                     finishOnKey="any digit", timeout=20) as g:
        # ask_grade = "{}, grade the state {} on the {}.".format(
        #     intros[num],
        #     'of California' if num <= 2 else '',
        #     statement_text[num],
        # )
        # g.say(ask_grade)
        g.play(url('statement-{}.mp3'.format(num+1)))

    return HttpResponse(str(resp))

# def demographic(request):
#     resp = twilio.twiml.Response()
#     with resp.gather(numDigits=5, action=reverse(peer_rate, args=[0]),
#                      finishOnKey="any digit", timeout=60) as g:
#             g.say("Would you like to join a discussion on what issue "
#                   "should be included on the next California Report Card")
#             g.pause(length=2)
#             g.say("Enter your zip code to continue.")
#     return HttpResponse(str(resp))

def peer_rate(request, num, cid): # num counts the number of questions that the participant rates
    # we need to add the comment id to the function definition.
    resp = twilio.twiml.Response()
    num = int(num)
    cid = int(cid)

    if cid > 0:
        # TODO: save Digits param for previous rating
        # os_save_rating
        rating = request.POST.get("Digits", "")
        # attempt to cast to an int?
        num_rating = -1
        try:
            num_rating = int(rating)
        except ValueError:
            pass
        callsid = request.POST.get("CallSid")
        username = find_username_from_CallSid(callsid)
        user = User.objects.get(username=username)
        cr = CommentAgreement(rater=user, comment=DiscussionComment.objects.get(id=cid), agreement=num_rating, is_current=True)
        cr.save()

        # value = -1
        # if (num_rating < 0 or num_rating > 4): # not a valid rating
        #     pass # Repeat the instructions
        # else:
        #     value = num_rating / 5.0
        #     # TODO: save Digits param for previous rating - Insight rating and agreement rating
        #     pass


    if num == 0:
        if not SHORT:
            resp.play(url('inst11.mp3'))
        cid, curl = get_comment()
        with resp.gather(numDigits=1, action=reverse(peer_rate, args=[num+1, cid]),
                         finishOnKey="any digit", timeout=15) as g:
            g.pause(length=2)
            g.play(curl)

    if num == 1:
        # resp.say("Just rate one more suggestion and then you can tell us yours", voice='alice')
        resp.play(url('inst12.mp3'))
        cid, curl = get_comment()
        with resp.gather(numDigits=1, action=reverse(peer_rate, args=[num+1, cid]),
                         finishOnKey="any digit", timeout=15) as g:
            # g.say("The suggestion is...", voice='alice')
            g.pause(length=2)
            g.play(curl)

    if num >= 2:
        resp.redirect(reverse(record_comment))

    return HttpResponse(str(resp))

def record_comment(request):
    resp = twilio.twiml.Response()
    # resp.say("Now, record your suggestion after the tone. Press any key when you're finished.", voice='alice')
    resp.play(url('inst13.mp3'))
    resp.pause(length=2)
    resp.record(action=reverse(finish), timeout=20, maxLength=20)
    return HttpResponse(str(resp))

def finish(request):
    # TODO: save Recording param for previous rating
    audio_recording = request.POST.get('RecordingUrl', '') # This is a wav file
    # os_id is not set. Does os_id = 1 work?
    # os_save_comment code
    username = find_username_from_CallSid(request.POST.get("CallSid", ""))
    user = User.objects.get(username = username)
    os_id = 1
    disc_stmt = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[0]

    #make a dummy comment
    if audio_recording:
        comment = DiscussionComment(user = user,
                                opinion_space_id = os_id,
                                discussion_statement = disc_stmt,
                                comment = audio_recording + ".mp3",
                                query_weight = -1,
                                is_current = True)
        comment.save()
    # fname = str(comment.id)
    #save the audio recording
    # save_audio(audio_recording, fname) # Does this work? Does this match the other function? What was data before?
    resp = twilio.twiml.Response()
    # resp.say("Thank you for completing the reproductive health survey. Please "
             # "encourage other women to take this survey too. Good bye! ", voice='alice')
    resp.play(url('inst14.mp3'))
    return HttpResponse(str(resp))

def save_audio(data, fname_prefix):
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    if fname_prefix.endswith(".wav"):
        fname = "audio/%s" % fname_prefix
    else:
        fname = "audio/%s.wav" % fname_prefix
    if default_storage.exists(fname):
        os.rename(settings.MEDIA_ROOT + fname,
                  settings.MEDIA_ROOT + default_storage.get_available_name(fname))
    path = default_storage.save(fname, ContentFile(data.read()))


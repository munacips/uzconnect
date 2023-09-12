from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from .models import Poll, PollNominee, Vote
from django.contrib.auth.decorators import login_required
from datetime import datetime, tzinfo
import pytz
utc = pytz.UTC


@login_required(login_url='/community/login/')
def home(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls,
    }
    return render(request,'votes/home.html',context)


@login_required(login_url='/community/login/')
def polldetails(request,id,*msg):
    poll = Poll.objects.get(id=id)
    nominees = PollNominee.objects.filter(poll=poll)
    context = {
        'poll' : poll,
        'nominees' : nominees,
        'msg' : msg
    }
    return render(request,'votes/polldetails.html',context)


@login_required(login_url='/community/login/')
def vote(request,id):
    nominee = PollNominee.objects.get(id=id)
    poll = nominee.getPoll()
    today = datetime.now()
    theday = poll.end_date
    today = today.replace(tzinfo=utc)
    theday = theday.replace(tzinfo=utc)
    if today > theday:
        return polldetails(request,poll.id,"NOT ALLOWED, DEADLINE PASSED !")
    try:
        new_vote, created = Vote.objects.get_or_create(voter=request.user,nominee=nominee,poll=poll)
    except:
        return polldetails(request,poll.id,"NOT ALLOWED !")
    return home(request)
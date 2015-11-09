from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from polls.models import Choice, Poll
from django.core.urlresolvers import reverse
#from django.template import RequestContext, loader

from polls.models import Poll

# Create your views here.
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, {'latest_poll_list': latest_poll_list,
    #                                  })
    context = {'latest_poll_list':latest_poll_list}
    #return HttpResponse(template.render(context))
    
    return render(request, 'polls/index.html', context)
    #return HttpResponse("Hello, world. You'are at the poll index")

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk = poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll':poll})

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
                                                     'pool':p,
                                                     'error_message': "You didn't select a choice.",
                                                     })
    else:
        selected_choice.votes += 1
        selected_choice.save();
        return HttpResponseRedirect(reverse('polls:results', args = (p.id,)))


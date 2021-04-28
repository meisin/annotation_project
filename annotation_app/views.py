from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# Create your views here.
from annotation_app.models import Sentences, Events, Event_arguments, Sent_validation, Event_validation

# Create your views here.

def index(request):
    ### Home page
    
    # Generate counts of sentences
    num_sent = Sentences.objects.count()
    num_sent_not_validated = Sent_validation.objects.filter(validated = 0).filter(annotator_id = request.user).count()
    num_event = Events.objects.count()
    num_event_not_validated = Event_validation.objects.filter(validated = 0).filter(annotator_id = request.user).count()
    
    context = {
        
        'num_sent': num_sent, 
        'num_sent_not_validated': num_sent_not_validated,
        'num_event': num_event,
        'num_event_not_validated': num_event_not_validated
    }
    
    return render(request, 'index.html', context = context)    

def EventsDescription(request):
    return render(request, 'events_description.html')

def EventsSchemas(request):
    return render(request, 'event_schemas.html')


def Glossary(request):
    return render(request, 'glossary.html')

'''
class SentencesListView(generic.ListView):
    model = Sentences
    context_object_name = 'sentences_list'
    paginate_by = 20
    
    def get_queryset(self):
        return Sentences.objects.filter(annotator_id = self.request.user).order_by('sent_id')    
'''

class Sent_validationListView(generic.ListView):
    model = Sent_validation
    context_object_name = 'sentences_list'
    paginate_by = 20
    
    def get_queryset(self):
        return Sent_validation.objects.filter(annotator_id = self.request.user).order_by('sent_id')
    
'''
class EventsListView(generic.ListView):
    model = Events
    paginate_by = 20
    context_object_name = 'events_list'
    
    def get_queryset(self):
        return Events.objects.filter(annotator_id = self.request.user).order_by('event_id')

'''

class Event_validationListView(generic.ListView):
    model = Event_validation
    context_object_name = 'events_list'
    paginate_by = 20
    
    def get_queryset(self):
        return Event_validation.objects.filter(annotator_id = self.request.user).order_by('event_id')

class UnvalidatedSentenceListView(generic.ListView):
    model = Sent_validation
    context_object_name = 'unvalidated_list'
    template_name = 'annotation_app/unvalidated_sentences_list.html'
    paginate_by = 20

    def get_queryset(self):           
        return Sent_validation.objects.filter(validated = 0).filter(annotator_id = self.request.user).order_by('sent_id')
    
    
class UnvalidatedEventListView(generic.ListView):
    model = Event_validation
    context_object_name = 'unvalidated_list'
    template_name = 'annotation_app/unvalidated_events_list.html'
    paginate_by = 20

    def get_queryset(self):           
        return Event_validation.objects.filter(validated = 0).filter(annotator_id = self.request.user).order_by('event_id')
    
    
### test out as equivalent to SentenceDetailView    
from annotation_app.forms import ValidateSentenceForm, ValidateEventForm

@login_required
def new_sentence_detail_view(request, pk):
    sent = get_object_or_404(Sentences, pk=pk)
    #sent = Sentences.objects.filter(annotator_id = request.user).select_related().get(pk = pk) 
    validation = Sent_validation.objects.filter(annotator_id = request.user).get(sent_id = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ValidateSentenceForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            #sent.review_comments = form.cleaned_data['review_comments']
            #sent.save
            validation.sent_validation_text = form.cleaned_data['review_comments']
            validation.validated = 1
            validation.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('unvalidated_sentences'))

    # If this is a GET (or any other method) create the default form
    else:
        
        if len(validation.sent_validation_text) == 0:
            initial_text = 'I agree fully with the annotation.'
        else:
            initial_text = validation.sent_validation_text
        
        form = ValidateSentenceForm(initial={'review_comments': initial_text})

    context = {
        'form': form,
        'sentences': sent
    }

    return render(request, 'annotation_app/sentences_detail2.html', context)
    
###########

@login_required
def new_event_detail_view(request, pk):
    #sent = get_object_or_404(Sentences, pk=pk)
    event = Events.objects.select_related().get(pk = pk)     
    event_sent = Events.objects.select_related('sent_id').get(pk=event.event_id) 
    sent = event_sent.sent_id

    validation = Event_validation.objects.select_related('event_id').filter(annotator_id = request.user).get(event_id = pk) 
 
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ValidateEventForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            validation.event_validation_text = form.cleaned_data['review_comments']
            validation.validated = 1
            validation.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('unvalidated_events'))

    # If this is a GET (or any other method) create the default form
    else:
        if len(validation.event_validation_text) == 0:
            initial_text = 'I agree fully with the annotation.'
        else:
            initial_text = validation.event_validation_text
        
        form = ValidateSentenceForm(initial={'review_comments': initial_text})
    context = {
        'form': form,
        'events': event,
        'sentences': sent
    }

    return render(request, 'annotation_app/events_detail.html', context)

###########


def sentence_detail_view(request):
    try:
        argument_event = Event_arguments.objects.select_related('event_id').get(id=1) 
        event = argument_event.event_id
        
        argument_sent = Events.objects.select_related('sent_id').get(pk=event.event_id) 
        sent = argument_sent.sent_id
        
    except Event_arguments.DoesNotExist:
        raise Http404('Argument does not exist')
        
    context = {
        'arg': argument_event,
        'event': event,
        'sent': sent
    }

    #print(len(arguments))
    return render(request, 'annotation_app/arg_detail.html', context)







###### Not needed anymore
  
class SentenceDetailView(generic.DetailView):
    model = Sentences

    
    
    
'''
BEFORE/CAUSES/PRECONDITIONS - EFFECT


CAUSES/PRECONDITIONS(main)
CAUSES/PRECONDITIONS(sub)


EFFECT (main)
EFFECT (sub)


Single EVent
'''


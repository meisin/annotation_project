from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events_desc/', views.EventsDescription, name='events_description'),
    path('glossary/', views.Glossary, name='glossary'),
    path('sentences/', views.Sent_validationListView.as_view(), name='sentences'),                  ## Class view
    path('sentence/<str:pk>', views.SentenceDetailView.as_view(), name='sentence-detail'),   ## Class view   ##### Not needed anymore
    path('unvalidated_sentences/', views.UnvalidatedSentenceListView.as_view(), name='unvalidated_sentences'),   ## Use class
    path('sentence_new/<str:pk>/validate/', views.new_sentence_detail_view, name='new-sentence-detail'),
    path('events/', views.Event_validationListView.as_view(), name='events'),
    path('unvalidated_events/', views.UnvalidatedEventListView.as_view(), name='unvalidated_events'),
    path('event/<str:pk>/validate/', views.new_event_detail_view, name='event-detail'),

    
]



### Not needed anymore
#     path('argument/', views.sentence_detail_view, name='arguments'),  ## Function view
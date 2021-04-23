from django.db import models
from django.urls import reverse   ## used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

# Create your models here.

class Sentences(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    #primary_key=True, default=uuid.uuid4, help_text='Unique ID for sentences') ## not used because do not want program to randomly assign ID.
    
    sent_id = models.CharField(max_length=300, primary_key=True, unique = True)
    text = models.TextField(max_length=1000)
    checked = models.BooleanField(default=False)    ## to delete
    sent_review_comments = models.TextField(max_length=1000, help_text='Enter your review/comments on the annotation', null=True, blank=True)  ## to delete    
    annotator_id = models.CharField(max_length=10, default='annotator1')    ## to delete
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('sentence-detail', args=[str(self.sent_id)])
 
    class Meta:
        ordering = ['sent_id']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.sent_id} ({self.text})'
    
class Events(models.Model):
    event_id = models.CharField(max_length=300, primary_key=True, unique = True)
    sent_id = models.ForeignKey('Sentences', on_delete=models.SET_NULL, null=True)
    polarity = models.CharField(max_length=8)    ##positive / negative
    polarity_cue = models.CharField(max_length=100, null=True)
    modality = models.CharField(max_length=8)     ##other / asserted
    modality_cue = models.CharField(max_length=100, null=True)    
    trigger = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    review_comments = models.TextField(max_length=1000, help_text='Enter your review / comments on the annotation', null=True, blank=True)
    annotator_id = models.CharField(max_length=10, default='annotator1')
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('event-detail', args=[str(self.event_id)])
    
    
    class Meta:
        ordering = ['event_id']
    
    def __str__(self):
        return f'{self.event_id} - {self.event_type}'
    
class Event_arguments(models.Model):
    event_id = models.ForeignKey('Events', on_delete=models.SET_NULL, null=True)
    entity_type = models.CharField(max_length=100)
    arg_text = models.CharField(max_length=300)
    arg_role = models.CharField(max_length=300)
    
    class Meta:
        ordering = ['event_id']
        
    def __str__(self):
        return f'{self.arg_role} - {self.arg_text}'
    
class Sent_validation(models.Model):
    sent_id = models.ForeignKey('Sentences', on_delete= models.SET_NULL, null=True)
    sent_validation_text = models.TextField(max_length=1000, help_text = 'Enter your review / comments on the annotation', null=True, blank=True)
    annotator_id = models.CharField(max_length = 10, default= 'annotator1')
    validated = models.IntegerField(default = 0)
    
    
class Event_validation(models.Model):
    event_id = models.ForeignKey('Events', on_delete = models.SET_NULL, null = True)
    event_validation_text = models.TextField(max_length=1000, help_text = 'Enter your review / comments on the annotation', null = True, blank = True)
    annotator_id = models.CharField(max_length = 10, default = 'annotator1')
    validated = models.IntegerField(default = 0)
    
    
    
    

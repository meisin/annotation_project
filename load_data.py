## python manage.py load_data

import random
from django.core.management.base import BaseCommand
from apps.annotation_app.models import Sentences, Events, Event_arguments
import pandas as pd

class Command(BaseCommand):
    """
    This command is for inserting Sentences, Events, Event_arguments into database.
    Read from excel files
    """
    def handle(self, *args, **options):
        #Sentences.objects.all().delete()
        #Events.objects.all().delete()
        #Event_arguments.objects.all().delete()
        
        
        ### Sentence ####
        sentence_df = pd.read_csv('sentence.csv')
        sentences = []
        for i in range(len(sentence_df)):
            print()
            sentences.append(Sentences(sent_id= sentence_df.iloc[i]['sentence_id'] , 
                                       text= sentence_df.iloc[i]['sentence'], 
                                       checked=False,    ### Not used - should be removed
                                       sent_review_comments=None, 
                                       annotator_id='annotator1'))

        Sentences.objects.bulk_create(sentences)
        
        '''        
        publishers = [Publisher(name=f"Publisher{index}") for index in range(1, 6)]
        Publisher.objects.bulk_create(publishers)

        # create 20 books for every publishers
        counter = 0
        books = []
        for publisher in Publisher.objects.all():
            for i in range(20):
                counter = counter + 1
                books.append(Book(name=f"Book{counter}", price=random.randint(50, 300), publisher=publisher))

        Book.objects.bulk_create(books)

        # create 10 stores and insert 10 books in every store
        books = list(Book.objects.all())
        for i in range(10):
            temp_books = [books.pop(0) for i in range(10)]
            store = Store.objects.create(name=f"Store{i+1}")
            store.books.set(temp_books)
            store.save()
        '''
        
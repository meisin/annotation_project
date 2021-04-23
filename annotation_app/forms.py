from django import forms

class ValidateSentenceForm(forms.Form):
    review_comments = forms.CharField(strip=True, widget=forms.Textarea(attrs={"rows":3, "cols":100}), help_text="Enter your comments / validation", initial="Agree with annotation                                                                                         ", required=True)
    
    
    
    
class ValidateEventForm(forms.Form):
    review_comments = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":100}), help_text="Enter your comments / validation", initial="Agree with annotation                                                                                         ", required=True)
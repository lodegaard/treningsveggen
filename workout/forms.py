from django import forms

class AddWorkoutForm(forms.Form):
    
    performed_date = forms.DateField(label='performed')
    comment = forms.CharField(label='comment')
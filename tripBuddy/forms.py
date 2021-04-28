from .models import Trip
from loginApp.models import User
from django import forms
from datetime import datetime
from django.forms.widgets import TextInput

class Date_In(TextInput):
    input_type = 'date'

class TripForm(forms.Form):
    destination = forms.CharField(max_length=200, widget=forms.TextInput)  
    start_date = forms.DateTimeField(widget=Date_In)
    end_date = forms.DateTimeField(widget=Date_In)
    details = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })

    def clean(self):
        super(TripForm, self).clean()
        destination = self.cleaned_data.get('destination')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        details = self.cleaned_data.get('details')

        def check_string(string, length, varName, message):
            if len(string) < length: 
                self.errors[f"{varName}"] = self.error_class([
                    f'{message}'])
                print('string failed')

        def check_date_after(date, compare, varName, message):            
            date_checking = date.replace(tzinfo=None)
            date_compared_to = compare.replace(tzinfo=None)
            if date_checking <= date_compared_to: 
                self.errors[f"{varName}"] = self.error_class([f'{message}'])
                print('label failed')           

        check_string(destination, 3, 'destination','Destination must contain at least 3 characters.')
        check_string(details, 3, 'details','Please provide a plan.')

        check_date_after(start_date, datetime.now(), 'start_date','Time travel is not allowed, our delorian is under repair.')
        check_date_after(end_date, start_date, 'end_date','End date is invalid.')
        
        return self.cleaned_data
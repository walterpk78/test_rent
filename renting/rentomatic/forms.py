from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django import forms
import logging


logger = logging.getLogger(__name__)


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class RentForm(forms.Form):
    transport_id  = forms.IntegerField( label="Transport Id", required=True)
    start_date    = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True)
    end_date      = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True)
    first_name	  = forms.CharField(widget=forms.TextInput(), label="First Name", required=True)
    last_name	  = forms.CharField(widget=forms.TextInput(), label="Last Name", required=True)
    phone         = forms.CharField(widget=forms.TextInput(), label="Phone", required=True)
    email	      = forms.CharField(widget=forms.TextInput(), label="E-mail", required=True)



class PaymentForm(forms.Form):
    amount            = forms.FloatField(widget=forms.TextInput(), label="Amount", required=True)
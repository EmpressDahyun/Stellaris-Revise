from django.contrib.auth import password_validation
from store.models import DeliveryInformation, ProductReservation, Reservation
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryInformation
        fields = ['fname','phone_number','barangay','landmark','location','notes']
        widgets = {
        'fname':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Juan Dela Cruz'}), 
        'phone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), 
        'barangay':forms.Select(attrs={'class':'form-control', 'placeholder':'Ex. Cabatangan'}),
        'landmark':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Cabatangan Elementary School'}),  
        'location':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Sitio Lumbang Along The Road'}),
        'notes':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Additional Notes, Request, Instructions'}),
        }

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'auto-focus':True, 'class':'form-control', 'placeholder':'Current Password'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Confirm Password'}))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['phone_number','pax','pax_expected', 'event_name','event_type','event_time','event_time_end','event_date','remarks']
        widgets = {'pax':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Number of Guest'}), 
        'phone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), 
        'pax':forms.Select(attrs={'class':'form-control', 'placeholder':'Ex. 30'}),
        'pax_expected':forms.Select(attrs={'class':'form-control', 'placeholder':'Ex. 30'}),
        'event_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Juan Dela Cruz 30th Birthday'}), 
        'event_type':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Birthday'}),
        'event_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
        'event_time_end':forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
        'event_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'remarks':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Please list the foods that you want to reserve in this box, or Additional Request, Suggestions, Notes.'}),
        }

class ProductReservationForm(forms.ModelForm):
    class Meta:
        model = ProductReservation
        fields = ['fname','phone_number','delivery_time','pickup_date','remarks']
        widgets = {
        'fname':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Juan Dela Cruz'}), 
        'phone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), 
        'delivery_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
        'pickup_date':forms.TimeInput(attrs={'class':'form-control', 'type':'date'}),  
        'remarks':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Additional Notes, Request, Instructions'}),
        }
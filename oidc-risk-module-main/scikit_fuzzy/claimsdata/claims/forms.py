from django import forms
from .models import ClaimTableEducation, ClaimTableOSP, Transaction

class ClaimTableEducationForm(forms.ModelForm):
    class Meta:
        model = ClaimTableEducation
        fields = '__all__'

class ClaimTableOSPForm(forms.ModelForm):
    class Meta:
        model = ClaimTableOSP
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
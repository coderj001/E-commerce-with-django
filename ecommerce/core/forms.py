from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_OPTION = (
        ('S','Stripe'),
        ('P','Paypal'),
    )

class CheckOutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1234 Main St','class':'form-control','id':'address'}))
    apparment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'apartment or suite','id':'address-2','class':'form-control'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':'custom-select d-block w-100'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'--zipcode--'}))
    same_shipping_address = forms.BooleanField()
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_OPTION)

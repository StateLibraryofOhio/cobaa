from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['inst_name', 'amount_requested']
        widgets = {
            'inst_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'amount_requested': forms.NumberInput(attrs={'min': '1', 'max': '2000', 'class': 'form-control'}),
            }


class OrderRetrieveForm(forms.Form):
    order_id = forms.CharField(label="Code",
                               max_length=6,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: HONQLA'}))

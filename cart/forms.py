from django import forms


class CartAddBookForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        widget=forms.NumberInput(attrs={'class': 'form-control-sm'})
        )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
        )

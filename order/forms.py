from django import forms
from order.models import Order,District
from accounts.models import Account

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        super().__init__(*args, **kwargs)

        # # initial-ları force tətbiq et
        # for field, value in initial.items():
        #     if field in self.fields:
        #         self.fields[field].initial = value

        self.fields['phone'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter address'
        self.fields['division'].widget.attrs['placeholder'] = 'Enter division'
        self.fields['district'].widget.attrs['placeholder'] = 'Enter district'
        self.fields['zip_code'].widget.attrs['placeholder'] = 'Enter zip code'
        self.fields['payment_method'].widget.attrs['placeholder'] = 'Payment method'
        self.fields['transaction_id'].widget.attrs['placeholder'] = 'Transaction ID'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'division', 'district', 'zip_code', 'payment_method',
                  'account_no', 'transaction_id']
        # xanayı deaktiv edir.
        widgets = {
            "account_no": forms.TextInput(attrs={"readonly": "readonly"})
        }
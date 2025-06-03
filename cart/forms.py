from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(label='Họ và tên', max_length=100)
    address = forms.CharField(label='Địa chỉ', widget=forms.Textarea)
    phone = forms.CharField(label='Số điện thoại', max_length=20)
    note = forms.CharField(label='Ghi chú', required=False, widget=forms.Textarea)

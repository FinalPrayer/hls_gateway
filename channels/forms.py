from django import forms


class ChannelAddForm(forms.Form):
    nickname = forms.CharField(
        widget=forms.TextInput(),
        label='Channel Nickname'
    )
    url = forms.CharField(
        widget=forms.Textarea(),
        label='Channel URL'
    )

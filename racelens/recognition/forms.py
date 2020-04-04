from django import forms
from .models import Photo, Selfie, Event


class UploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

    # def __init__(self, user, *args, **kwargs):
    #     super(UploadForm, self).__init__(*args, **kwargs)
    #     self.fields['event'].queryset = Event.objects.filter(user=user)


class UploadSelfie(forms.ModelForm):
    class Meta:
        model = Selfie
        fields = ['image']


class CreateEvent(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'poster']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=500, label="Nombre")
    mail = forms.EmailField(max_length=500, label="Correo")
    subject = forms.CharField(max_length=200, label="Asunto")
    message = forms.CharField(label='Mensaje',widget=forms.Textarea(
                        attrs={'placeholder': 'Escribe tu mensaje'}))
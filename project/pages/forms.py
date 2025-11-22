from django import forms
from .models import ContactMessage

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject']  # فقط حقل الموضوع
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع الرسالة'
            }),
        }
        labels = {
            'subject': 'الموضوع',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # استلام المستخدم من الخارج
        super(ContactForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.instance.name = user.get_full_name()  # تعبئة الاسم تلقائيًا





from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
       class Meta:
           model = Profile
           fields = ['age', 'mobile_phone', 'subscription', 'image', 'has_visited']
from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError

def validate_media(form_cleaned_data):
    img = form_cleaned_data.get('image')
    vid = form_cleaned_data.get('video')
    content = form_cleaned_data.get('content')
    if not content and not img and not vid:
        raise ValidationError("Gönderi en azından metin, resim veya video içermelidir.")
    if img and vid:
        raise ValidationError("Aynı anda hem resim hem video yükleyemezsiniz (isteğe bağlı).")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'placeholder':'Ne düşünüyorsun?', 'class':'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        validate_media(cleaned)
        return cleaned

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':2, 'class':'form-control', 'placeholder':'Yorum yaz...'}),
        }


def clean_image(self):
    img = self.cleaned_data.get('image')
    if img:
        if img.size > 5*1024*1024:
            raise forms.ValidationError("Resim 5MB'dan büyük olamaz.")
        if not img.content_type.startswith('image/'):
            raise forms.ValidationError("Geçerli bir resim dosyası yükleyin.")
    return img
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class UserModel(models.Model):
    username = models.CharField(unique=True, max_length=25, validators=[MinLengthValidator(4)])
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8), MaxLengthValidator(24)])  # Şifrelenmiş parola için alan

    def clean(self):
        if len(self.username) < 4:
            raise ValidationError("Kullanıcı adı en az 4 karakter olmalıdır.")

    def save(self, *args, **kwargs):
        self.full_clean()  # clean() metodunu çağırarak model doğrulamasını yap
        
        # Parolayı şifrele ve kaydet (sadece yeni parola belirtilmişse)
        if self.password and not self.password.startswith('sha256$'):  # Parola zaten şifrelenmişse tekrar şifreleme
            self.password = make_password(self.password)
        
        super(UserModel, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Parolayı doğrula

    def __str__(self):
        return self.username

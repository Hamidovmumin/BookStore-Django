from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number,password=None):
        if not email:
            raise ValueError('The email must be set')
        if not username:
            raise ValueError('The username must be set')

        user = self.model(
            email=self.normalize_email(email),  # email-in düzgün formata salınması üçün istifadə olunur.
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)  # parolu təhlükəsiz formada saxlamaq üçün istifadə olunur (hash-lənir).
        user.save(using=self._db)  # istifadəçini verilənlər bazasında saxlayır.
        return user

    def create_superuser(self, first_name, last_name, username,phone_number, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Create your models here.

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)  # istifadəçinin qeydiyyat vaxtı.
    last_login = models.DateTimeField(auto_now=True)  # son giriş vaxtı.
    is_admin = models.BooleanField(default=False)  # icazəsi var, amma mütləq deyil ki, superuser-dir.
    is_active = models.BooleanField(default=False)  # istifadəçi aktivdirsə True olmalıdır.
    is_staff = models.BooleanField(default=False)  # admin panelə daxil ola bilər.
    is_superadmin = models.BooleanField(default=False)  # tam icazəyə sahib admin.

    USERNAME_FIELD = 'email'  # İstifadəçi login olmaq üçün email istifadə edəcək.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_number']  # createsuperuser komutu zamanı bu sahələr də tələb olunacaq.

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # Asagikadki iki metodlar yazılmazsa, kod işləyər, amma admin panel və icazə sistemi etibarlı olmaz.Admin panelə
    # girişdə və icazə yoxlamalarında bəzi problemlərlə qarşılaşa bilərsən.
    # Ona görə yazmaq tövsiyə olunur, xüsusən AbstractBaseUser istifadə edəndə.

    def has_perm(self, perm, obj=None):  # İstifadəçinin müəyyən bir icazəyə sahib olub olmadığını yoxlayır.
        return self.is_admin

    def has_module_perms(self, add_label):
        return True












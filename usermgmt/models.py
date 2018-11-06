# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        extra_fields.setdefault('staff', True)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('admin', True)
        user = self.create_user(email, password, **extra_fields)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=64, blank=True)
    firstname = models.CharField(max_length=128, blank=True)
    lastname = models.CharField(max_length=128, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    objects = UserManager()


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "personal_info"), on_delete=models.CASCADE)
    address1 = models.TextField(_("address1"))
    address2 = models.TextField(_("address2"), blank=True, null=True)
    secondary_email = models.EmailField(
        _("secondary_email"), max_length=254, blank=True, null=True)
    mobile_number = models.CharField(_("mobile_number"), max_length=20)
    state = models.CharField(_("state"), max_length=200, blank=True, null=True)
    city = models.CharField(_("city"), max_length=200, blank=True, null=True)
    country = models.CharField(
        _("country"), max_length=200, blank=True, null=True)
    dob = models.DateTimeField(
        _("dob"), auto_now=False, auto_now_add=False, blank=True, null=True)
    gender = models.CharField(
        _("gender"), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(
        _("created_at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("updated_at"), auto_now=True, auto_now_add=False)

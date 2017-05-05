# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.core import mail
from apps.edu.models import Major, Field

from apps.accounts.views import UpdateProfileView
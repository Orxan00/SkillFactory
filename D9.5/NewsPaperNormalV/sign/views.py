from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BasicSignupForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
import sys

sys.path.append('..')

from news.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BasicSignupForm
    success_url = '/news/'

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)

    Author.objects.create(user=user)

    return redirect('/news/')


def welcome(instance, **kwargs):

    send_mail(
        subject=f'Здравствуй {instance.email}',
        message='Спасибо за регитсрацию!',
        from_email='smd1@yandex.ru',
        recipient_list=[instance.email],
    )

post_save.connect(welcome, sender=User)

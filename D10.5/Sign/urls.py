from django.urls import path
from .views import upgrade_me, IndexView


urlpatterns = [
    path('authors/', IndexView.as_view(template_name = 'sign/authors.html'),
         name='authors'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
]
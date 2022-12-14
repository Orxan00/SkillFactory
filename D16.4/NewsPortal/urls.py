from django.urls import path
from .views import PostList, PostDetail, SearchList, AddList, PostUpdateView, PostDeleteView, AddSubscribers
 
 
urlpatterns = [
    path('', PostList.as_view()),
    path('search/', SearchList.as_view()),
    path('add/', AddList.as_view()),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>', PostDetail.as_view(), name='new'),
    path('subscribers/<int:pk>', AddSubscribers.as_view(), name= 'add_subscribers'),

]
from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostEdit, PostDelete, CategoriesView, CategoryDetail, subscribe_to_category

urlpatterns = [
    path("", PostsList.as_view(), name='post_list'),
    path("<int:pk>", PostDetail.as_view()),
    path('create/', PostCreate.as_view()),
    path('search/', PostSearch.as_view()),
    path("<int:pk>/edit/", PostEdit.as_view()),
    path("<int:pk>/delete/", PostDelete.as_view()),
    path("categories/", CategoriesView.as_view()),
    path("categories/<int:pk>", CategoryDetail.as_view()),
    path("categories/<int:pk>/subscribe", subscribe_to_category),
]
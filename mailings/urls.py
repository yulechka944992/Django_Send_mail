from django.urls import path
from . import views

app_name = 'mailings'

urlpatterns = [
    path('', views.MessageListView.as_view(), name='message_list'),
    path('create/', views.MessageCreateView.as_view(), name='message_create'),
    path('<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
]
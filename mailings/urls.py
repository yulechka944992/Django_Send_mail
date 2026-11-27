from django.urls import path
from . import views

app_name = 'mailings'

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<int:pk>/update/', views.CampaignUpdateView.as_view(), name='campaign_update'),
    path('campaigns/<int:pk>/delete/', views.CampaignDeleteView.as_view(), name='campaign_delete'),
    path('campaigns/<int:pk>/send/', views.start_campaign, name='campaign_send'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics')
]
from django.utils import timezone

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib import messages

from recipients.models import Recipient
from .forms import CampaignForm
from .models import Message, Campaign
from .services import send_campaign


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')


class CampaignListView(ListView):
    model = Campaign
    template_name = 'mailings/campaign_list.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        queryset = super().get_queryset()
        for campaign in queryset:
            campaign.update_status()
        return queryset

class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'mailings/campaign_form.html'
    success_url = reverse_lazy('mailings:campaign_list')

class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'mailings/campaign_detail.html'
    context_object_name = 'campaign'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

class CampaignUpdateView(UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'mailings/campaign_form.html'
    success_url = reverse_lazy('mailings:campaign_list')

class CampaignDeleteView(DeleteView):
    model = Campaign
    template_name = 'mailings/campaign_confirm_delete.html'
    success_url = reverse_lazy('mailings:campaign_list')


def start_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    campaign.update_status()

    is_success, result_message = send_campaign(campaign)

    if is_success:
        messages.success(request, result_message)
    else:
        messages.error(request, result_message)

    return redirect('mailings:campaign_detail', pk=campaign.pk)


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['total_campaigns'] = Campaign.objects.count()

        context['active_campaigns_count'] = Campaign.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status='Запущена'
        ).count()

        context['total_recipients'] = Recipient.objects.count()

        return context


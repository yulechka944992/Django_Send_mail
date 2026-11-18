from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Recipient

class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipients/recipient_list.html'
    context_object_name = 'recipients'

class RecipientCreateView(CreateView):
    model = Recipient
    fields = ['email', 'last_name', 'first_name', 'comment']
    template_name = 'recipients/recipient_form.html'
    success_url = reverse_lazy('recipients:list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'last_name', 'first_name', 'comment']
    template_name = 'recipients/recipient_form.html'
    success_url = reverse_lazy('recipients:list')

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'recipients/recipient_detail.html'
    context_object_name = 'recipient'

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'recipients/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipients:list')
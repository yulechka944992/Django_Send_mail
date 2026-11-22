from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from recipients.models import Recipient

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Campaign(models.Model):
    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    status = models.CharField(max_length=20, blank=True, null=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка #{self.pk} ({self.message.subject})"

    def update_status(self):
        now = timezone.now()
        new_status = ''

        if now < self.end_time:
            new_status = 'Создана'
        elif self.start_time <= now <= self.end_time:
            new_status = 'Запущена'
        else:
            new_status = 'Завершена'

        if self.status != new_status:
            self.status = new_status
            self.save()

    def clean(self):
        super().clean()
        now = timezone.now()

        if self.start_time and self.start_time < now:
            raise ValidationError({'start_time': 'Дата начала не может быть в прошлом.'})

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({'end_time': 'Дата окончания должна быть позже даты начала.'})


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='attempts', verbose_name="Рассылка")
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name="Получатель")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"

    def __str__(self):
        return f"{self.mailing.pk} -> {self.recipient.email} ({self.status})"
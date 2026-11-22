from itertools import batched

from django.utils import timezone
from django.core.mail import send_mail
from .models import Attempt


def send_campaign(campaign, batch_size=100):
    """
    Проверяет время и рассылает письма.
    Возвращает кортеж (успех_булево, текст_сообщения)
    """
    now = timezone.now()

    if not (campaign.start_time <= now <= campaign.end_time):
        return False, "Ошибка: Текущее время находится вне интервала рассылки."

    recipients = campaign.recipients.all()
    if not recipients:
        return False, "Ошибка: У рассылки нет получателей."

    subject = campaign.message.subject
    body = campaign.message.body
    success_count = 0
    error_count = 0

    for batch in batched(recipients, batch_size):
        attempts_to_create = []

        for recipient in batch:
            try:
                sent_count = send_mail(subject, body, None, [recipient.email], fail_silently=False)
                attempts_to_create.append(
                    Attempt(
                        mailing=campaign,
                        recipient=recipient,
                        status='Успешно',
                        server_response=f"Письмо успешно принято сервером. Код ответа: {sent_count}"
                    )
                )
                success_count += 1
            except Exception as e:
                attempts_to_create.append(
                    Attempt(mailing=campaign,
                            recipient=recipient,
                            status='Не успешно',
                            server_response=str(e)
                    )
                )
                error_count += 1

        Attempt.objects.bulk_create(attempts_to_create)

    return True, f"Рассылка завершена. Успешно: {success_count}, Ошибок: {error_count}."
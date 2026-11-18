from django.db import models

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"
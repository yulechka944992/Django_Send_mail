from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from .forms import RegisterForm
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_url = self.request.build_absolute_uri(
            reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
        )

        subject = 'Registration confirmation'
        message = f'Hello, {user.username}!\n\nPlease activate your account here:\n{activation_url}'

        print("\n" + "=" * 50)
        print(f"ТЕМА: {subject}")
        print(f"КОМУ: {user.email}")
        print(f"ТЕКСТ:\n{message}")

        send_mail(
            subject,
            message,
            'noreply@mail-service.ru',
            [user.email],
            fail_silently=False,
        )

        messages.success(self.request, "Регистрация успешна! Проверьте вашу почту (в терминале) для подтверждения.")
        return redirect(self.success_url)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Ваш аккаунт успешно активирован! Теперь вы можете войти.")
    else:
        messages.error(request, "Ссылка для активации недействительна или устарела.")

    return redirect('accounts:login')


class CustomPasswordResetView(PasswordResetView):
    """Переопределяем встроенный класс Django, для вывода человекочитаемого письма"""
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        response = super().form_valid(form)

        email = form.cleaned_data['email']
        from django.contrib.auth.models import User
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://127.0.0.1:8000/accounts/reset/{uid}/{token}/"
            print("\n" + "=" * 50)
            print(f"ССЫЛКА ДЛЯ СБРОСА ПАРОЛЯ ({email}):")
            print(reset_url)
            print("=" * 50 + "\n")
        except User.DoesNotExist:
            pass

        return response


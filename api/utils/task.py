from .smtp_email_backend import SmtpEmailBackend


def send_email_newsletter(client_name):
    email_backend = SmtpEmailBackend(
        smtp_server="localhost",
        smtp_port=1025,
        from_email="noreply@test.com",
    )

    email_backend.send_email(
        recipient="example@gmail.com",
        subject="Вы успешно зарегистрировались!",
        body=f"Hello {client_name}!",
    )
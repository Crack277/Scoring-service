from .task import send_email_newsletter


def send_email_task():
    send_email_newsletter.delay()
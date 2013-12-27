from models import Notification
from django.core.mail import send_mail

EMAIL_THRESHOLD = 2


def notify(sender, receptors, message, url, level=1, **kwargs):
    """
    receptors: list of user instances
    """
    notifications = []
    receptor_emails = []
    for receptor in receptors:
        notification = Notification(
            sender=sender,
            receptor=receptor,
            message=message,
            url=url,
            level=level,
        )
        notification.save()
        notifications.append(notification)
        receptor_emails.append(receptor.email)

    if level < EMAIL_THRESHOLD:
        send_mail(
            message, url, sender.email, receptor_emails, fail_silently=False)

    return notifications

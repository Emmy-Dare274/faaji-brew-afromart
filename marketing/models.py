import uuid
from django.db import models


class NewsletterSubscriber(models.Model):
    """A newsletter signup. Confirmation works the same way as
    account email verification, a real email with a real link."""

    email = models.EmailField(unique=True)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
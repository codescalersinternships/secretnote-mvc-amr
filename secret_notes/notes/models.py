from django.db import models
from django.utils import timezone
import uuid

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateTimeField()
    views = models.IntegerField(default=0)
    max_views = models.IntegerField(default=1)

    def is_expired(self):
        return timezone.now() >= self.exp_date or self.views >= self.max_views

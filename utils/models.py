from django.db import models
from simple_history.models import HistoricalRecords
import uuid

class BaseModel(models.Model):

    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
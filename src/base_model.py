from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet

from src.enums import LogEntryEnum


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado em")

    class Meta:
        abstract = True

    def add_log_entry(self, user_id: str, reason: str, flag: LogEntryEnum) -> None:
        LogEntry.objects.log_action(
            user_id=user_id,
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.pk,
            object_repr=str(self),
            action_flag=flag,
            change_message=f"Desativado por: {reason}",
        )

    def list_log_entries(self) -> QuerySet[LogEntry]:
        content_type = ContentType.objects.get_for_model(self)
        queryset = LogEntry.objects.filter(content_type=content_type, object_id=str(self.pk))
        return queryset

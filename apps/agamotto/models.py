from django.db import models
from django.utils import timezone
from apps.core.models import Base


class ScheduledTask(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    task = models.CharField("Tarefa", max_length=100, blank=False, null=False)
    status = models.CharField("Status", max_length=100, blank=False, null=False)
    gv_code = models.IntegerField('GV Code', blank=True, null=True)
    extra_field = models.CharField("Extra", max_length=200, blank=True, null=True)
    error_message = models.CharField("Erro", max_length=500, blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.task + ' - ' + self.status

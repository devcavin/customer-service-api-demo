from django.db import models
from django.utils.translation import gettext_lazy as _
from project.utils import format_datetime
# Create your models here.


class Notes(models.Model):
    """Class notes etc"""

    title = models.CharField(help_text=_("Content title"), max_length=200)
    content = models.TextField(help_text=_("Notes in detail"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Date and time when entry was first made"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Date and time when entry was updated"))

    class Meta:
        verbose_name = _("Notes")
        verbose_name_plural = _("Notes")


    def model_dump(self):
        return dict(
            id = self.id,
            title= self.title,
            content = self.content,
            created_at = format_datetime(self.created_at)
        )
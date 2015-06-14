from django.db import models


class Entry(models.Model):
    value = models.CharField(max_length=150)
    parent_ref = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.value

    def get_root(self):
        if self.parent_ref is None:
            return self
        else:
            return self.parent_ref.get_root()

    def get_ancestors(self):
        if self.parent_ref is None:
            return Entry.objects.none()
        return Entry.objects.filter(pk=self.parent_ref.pk) | self.parent_ref.get_ancestors()

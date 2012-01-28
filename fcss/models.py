from django.db import models
from django.template.defaultfilters import slugify

class Stylesheet(models.Model):
    title = models.CharField(max_length=50)
    filename = models.CharField(max_length=50, blank=True, help_text='Without leading slash. This will automatically have <strong>.css</strong> added to the end.')
    css = models.TextField('CSS', help_text='Enter some CSS here')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.filename or len(self.filename.strip()) == 0:
            self.filename = slugify(self.title)

        super(Stylesheet, self).save()

    class Meta:
        ordering = ['title']

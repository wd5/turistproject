from django import template
from django.conf import settings
from fcss.models import Stylesheet
from datetime import datetime
import os

register = template.Library()

def get_css(title):
    title = title.strip('"')

    try:
        sheet = Stylesheet.objects.get(title=title)
    except Stylesheet.DoesNotExist:
        raise template.TemplateSyntaxError('%s is an invalid stylesheet' % title)

    parse = False
    modified = None
    file = '%s.css' % sheet.filename
    output = os.path.join(settings.STATIC_ROOT, file)
    path = os.path.abspath(output)

    try:
        os.makedirs(path)
    except OSError:
        pass

    try:
        modified = datetime.fromtimestamp(os.path.getmtime(output))
    except OSError:
        pass

    if not modified or (modified and modified < sheet.date_updated):
        parse = True

    if parse:
        try:
            f = open(output, 'w')
            f.write(sheet.css)
            f.close()
        except IOError:
            raise template.TemplateSyntaxError('Failed to write %s' % output)
    return '%s%s' % (settings.STATIC_URL, file)

register.simple_tag(get_css)

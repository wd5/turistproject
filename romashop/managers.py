from django.db.models import Manager
from datetime import datetime


class PublicManager(Manager):
    """Returns published items"""

    def published(self):
        return self.get_query_set().filter(is_published=True)


class DiscountManager(Manager):
    """Returns active items"""

    def get_query_set(self):
        date_now = datetime.now()
        return super(DiscountManager, self).get_query_set().filter(is_active=True).filter(date_start__lt=date_now).filter(date_end__gt=date_now)

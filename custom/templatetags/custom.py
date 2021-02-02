import datetime
from dateutil.relativedelta import relativedelta
from django import template

register = template.Library()

@register.simple_tag
def last_month():
    last_month = datetime.datetime.now() - relativedelta(month=1)
    return datetime.datetime.strftime(last_month, "%Y-%m")
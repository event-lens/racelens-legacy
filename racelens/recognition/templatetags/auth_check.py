from django import template

register = template.Library()


@register.filter(name='is_staff')
def is_staff(user):
    return user.groups.filter(name='staff').exists()

@register.filter(name="is_event_owner")
def is_event_owner(user, event):
    return event.user == user
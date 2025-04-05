from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Custom template filter to check if a user belongs to a specific group.
    Usage in template: {% if user|has_group:"Group Name" %}
    """
    return user.groups.filter(name=group_name).exists()

from django import template

register = template.Library()

bulma_map = {
    'debug': 'is-link',
    'info': 'is-info',
    'success': 'is-success',
    'warning': 'is-warning',
    'error': 'is-danger',
}

@register.filter(name="convert")
def convert(value):
    if value in bulma_map:
        return bulma_map[value] or ''
    return ''

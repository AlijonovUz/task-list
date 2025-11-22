from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_classes):
    existing_classes = field.field.widget.attrs.get('class', '')
    new_classes = f"{existing_classes} {css_classes}".strip()
    return field.as_widget(attrs={'class': new_classes})


@register.filter(name='is_invalid')
def is_invalid(field, class_name):
    existing = field.field.widget.attrs.get('class', '')

    if field.errors:
        new_class = f"{existing} {class_name}".strip()
    else:
        new_class = existing

    return field.as_widget(attrs={'class': new_class})
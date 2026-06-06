from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    existing_classes = field.field.widget.attrs.get("class", "")
    classes = f"{existing_classes} {css_class}".strip()
    return field.as_widget(attrs={"class": classes})


@register.filter
def is_checkbox(field):
    return getattr(field.field.widget, "input_type", "") == "checkbox"


@register.filter
def is_select(field):
    return getattr(field.field.widget, "input_type", "") == "select"

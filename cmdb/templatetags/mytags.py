# coding: utf-8


from django import template

register = template.Library()


@register.filter(name='int2str')
def int2str(value):
    """
    int 转换为 str
    """
    return str(value)


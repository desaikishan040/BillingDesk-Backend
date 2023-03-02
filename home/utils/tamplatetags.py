from django import template

register = template.Library()


def encrypt(value):  # Only one argument.
    value = int(value)
    value = value << 69

    return value


def decrypt(value):
    value = int(value)
    value = value >> 69

    return value


register.filter('encrypt', encrypt)

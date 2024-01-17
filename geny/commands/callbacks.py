from geny.core.utils import sanitized_string


def sanitized_string_callback(ctx, param, value):
    return sanitized_string(value)

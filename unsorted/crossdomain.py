from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if not type(origin) == 'str':
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()


    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = 'HEAD, GET, DELETE, POST, OPTIONS'
            h['Access-Control-Max-Age'] = str(max_age)

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

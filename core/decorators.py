from django.core.exceptions import PermissionDenied


def staff_required(view_func):

    """ A single place to define what 'staff' means for the
    front-end staff tools, so review moderation now and staff
    product management next (#29) don't each repeat the same
    is_staff check. Raises a plain 403 rather than redirecting to
    the Django admin login, since these are front-end pages. """

    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped

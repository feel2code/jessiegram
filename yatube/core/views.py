from django.shortcuts import render
from http.client import NOT_FOUND, FORBIDDEN, INTERNAL_SERVER_ERROR


html_renders = {
    'csrf': 'core/403csrf.html',
    '403': 'core/403.html',
    '404': 'core/404.html',
    '500': 'core/500.html',
}


def csrf_failure(request, reason=''):
    return render(
        request,
        html_renders['csrf']
    )


def permission_denied(request, exception):
    return render(
        request,
        html_renders['403'],
        status=FORBIDDEN
    )


def page_not_found(request, exception):
    return render(
        request,
        html_renders['404'],
        {'path': request.path},
        status=NOT_FOUND
    )


def server_error(request):
    return render(
        request,
        html_renders['500'],
        status=INTERNAL_SERVER_ERROR
    )

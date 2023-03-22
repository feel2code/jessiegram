from django.core.paginator import Paginator
from django.conf import settings


def paginator_module(request, post_list):
    paginator = Paginator(post_list, settings.LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

from django.core.paginator import Paginator, EmptyPage

def paginate_posts(request, queryset, posts_per_page=10):
    paginator = Paginator(queryset, posts_per_page)
    
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return page_obj
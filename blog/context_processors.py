from .models import Category

def site_info(request):
    return {
        'site_name': 'The Readers Hut',
        'site_description': 'Books, Reviews, and Reading Community',
        'categories': Category.objects.all(),
    }
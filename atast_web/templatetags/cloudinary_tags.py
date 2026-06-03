from django import template

register = template.Library()

@register.filter
def cloudinary_optimize(url):
    """Insert f_auto,q_auto,w_auto into a Cloudinary URL for automatic format/quality."""
    if not url or 'res.cloudinary.com' not in str(url):
        return url
    url = str(url)
    if '/upload/' in url and 'f_auto' not in url:
        url = url.replace('/upload/', '/upload/f_auto,q_auto/', 1)
    return url

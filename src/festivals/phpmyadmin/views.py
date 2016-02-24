import mimetypes

from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from festivals.utils import (
    APRIL_FOOL_COOKIE_KEY, APRIL_FOOL_COOKIE_DONE_VALUE,
    get_tomorrow,
)

from .forms import PHPMyAdminLogInForm


def index(request):
    if request.method == 'POST':
        form = PHPMyAdminLogInForm(request.POST)
        if form.is_valid():
            form.save()
            response = redirect(request.COOKIES.get(
                APRIL_FOOL_COOKIE_KEY, reverse('index'),
            ))
            response.set_cookie(
                APRIL_FOOL_COOKIE_KEY, APRIL_FOOL_COOKIE_DONE_VALUE,
                expires=get_tomorrow(),
            )
            return response
    return render(request, 'festivals/phpmyadmin/login.html', {})


def staticfile(request, path):
    """Resolve static files for PHPMyAdmin view.

    For maximum likeliness, statis paths in the PHPMyAdmin view use original
    values from the real implementation. This view is designed specifically to
    resolve those into files inside the static directory.
    """
    filename = path.split('/')[-1]
    if filename.endswith('.php'):
        filename = filename[:-4]
    real_path = finders.find(
        'festivals/phpmyadmin/{filename}'.format(filename=filename),
    )
    if real_path is None:
        return HttpResponse()
    content_type = mimetypes.guess_type(real_path)
    with open(real_path, 'rb') as f:
        return HttpResponse(f.read(), content_type=content_type[0])


def url_redirect(request):
    """Mimic PHPMyAdmin's `url.php`.
    """
    href = request.GET.get('url')
    return redirect(href)

import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .utils import (
    APRIL_FOOL_COOKIE_KEY, APRIL_FOOL_COOKIE_DONE_VALUE,
    get_tomorrow,
)


class AprilFoolMiddleware:
    """Redirect to April Fools' Day event page by on the date.

    For ease of testing, the redirection also happens if the request contains
    a special query key `shigatsu`.
    """
    response_redirect_class = HttpResponseRedirect

    def _is_april_fool(self, request):
        today = datetime.date.today()
        return (
            (today.month == 4 and today.day == 1)
            or 'shigatsu' in request.GET
        )

    def _should_redirect(self, request):
        cookie = request.COOKIES.get(APRIL_FOOL_COOKIE_KEY, '')
        return self._is_april_fool() and cookie != APRIL_FOOL_COOKIE_DONE_VALUE

    def process_request(self, request):
        if request.path.startswith('/phpmyadmin/'):
            return
        if not self._should_redirect(request):
            return
        response = self.response_redirect_class(reverse('phpmyadmin_index'))
        response.set_cookie(
            APRIL_FOOL_COOKIE_KEY, request.path,
            expires=get_tomorrow(),
        )
        return response

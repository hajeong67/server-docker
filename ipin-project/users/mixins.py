from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin

# middleware의 역할
class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = 'Page not found'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('pypackages:current-time')


class LoggedInOnlyView(AccessMixin):
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
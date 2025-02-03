from django.shortcuts import redirect, reverse
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from .forms import LoginForm
from .mixins import LoggedOutOnlyView


decorators = [never_cache,]

# 데코레이터 이용해서 -> 캐싱 막음 (로그인하고 뒤로가는 상황)
@method_decorator(decorators, name='dispatch')
class LoginView(LoggedOutOnlyView, FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get('next')
        return next_arg if next_arg else reverse('pypackages:current-time') # 한 단계 위에서 검색, 뷰를 랜더링


@never_cache
def log_out(request):
    logout(request)
    return redirect(reverse('users:login')) # 루트에서 검색, 리다이렉트만

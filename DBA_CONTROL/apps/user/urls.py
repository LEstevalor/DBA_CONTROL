from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^email_codes/$', views.EmailVerifyView.as_view()),  # 邮箱验证
    # url(r"/register$", )
)

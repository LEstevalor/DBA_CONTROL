from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^email_codes/$', views.EmailVerifyView.as_view()),  # 邮箱验证

    url(r'^user_register/$', views.RegisterUserView.as_view()),  # 注册功能

    url(r'^unique/', views.UniqueView.as_view()),  # 检查账号或邮箱是否注册过
)

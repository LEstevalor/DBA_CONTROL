from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^email_codes/$', views.EmailSendView.as_view()),  # 邮箱验证码发送
    url(r'^check_email_codes/$', views.EmailVerifyView.as_view()),  # 邮箱验证码验证

    url(r'^user_register/$', views.RegisterUserView.as_view()),  # 注册功能

    url(r'^unique/$', views.UniqueView.as_view()),  # 检查账号或邮箱是否注册过

    url(r'^login/$', views.LoginTokenView.as_view(), name='token_obtain_pair'),     # JWT登录功能
)

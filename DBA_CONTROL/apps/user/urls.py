from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^email_codes/$', views.EmailSendView.as_view()),  # 邮箱验证码发送
    url(r'^check_email_codes/$', views.EmailVerifyView.as_view()),  # 邮箱验证码验证

    url(r'^user_register/$', views.RegisterUserView.as_view()),  # 注册功能

    url(r'^unique/$', views.UniqueView.as_view()),  # 检查账号或邮箱是否注册过

    url(r'^login/$', views.LoginTokenView.as_view(), name='token_obtain_pair'),     # JWT登录功能

    url(r'^get_username_realname/$', views.RealNameView.as_view()),  # 获取真实姓名

    url(r'^check_user/$', views.UserView.as_view()),  # 判断前端用户状态是否正确

    url(r'^status/$', views.StatusView.as_view()),  # 获取权限级别

    url(r'^resetPassword/$', views.ResetPassword.as_view())  # 重置密码
)

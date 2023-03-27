# from django.conf.urls import url
from rest_framework import routers

from . import views

# urlpatterns = (
# )

router = routers.DefaultRouter()
router.register(r'college', views.CollegeViewSet, basename="college")  # 学院信息视图
router.register(r'major', views.MajorViewSet, basename="major")  # 专业信息视图
router.register(r'teacher', views.TeacherViewSet, basename="teacher")  # 教师信息视图
router.register(r'student', views.StudentViewSet, basename="student")  # 学生信息视图
urlpatterns = router.urls
# urlpatterns += router.urls

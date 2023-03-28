from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'courses', views.CoursesViewSet, basename="courses")  # 课程信息视图
router.register(r'student_course', views.StudentCourseViewSet, basename="student_course")  # 学生课程信息视图
urlpatterns = router.urls

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'teach_student_class', views.TeachStudentClassViewSet, basename="teach_student_class")  # 教研室信息视图
router.register(r'grade', views.GradeViewSet, basename="grade")  # 班级信息视图
urlpatterns = router.urls

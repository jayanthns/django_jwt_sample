from django.conf.urls import url

from .views import (CreateUserAPIView, LoginAPIview, PersonalInfoAPIView,
                    UserDetailsAPIVew)

urlpatterns = [
    url(r"^register", CreateUserAPIView.as_view(), name="create_user"),
    url(r"^login", LoginAPIview.as_view(), name="login_user"),
    url(r"^detail", UserDetailsAPIVew.as_view(), name="user_detail"),
    url(r"^personal-info", PersonalInfoAPIView.as_view(), name="personal_info"),
]

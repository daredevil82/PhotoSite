from __future__ import absolute_import

from django.conf.urls import url

from app.views.access import LoginView, LogoutView, RegistrationView
from app.views.company import CompanyDetailView, CompanyListView
from app.views.item import UploadItemView
from app.views.user import UserDetailView, UserListView

urlpatterns = [
    url(r'^login$', LoginView.as_view(), name = 'Login View'),
    url(r'^logout$', LogoutView.as_view(), name = 'Logout View'),
    url(r'^register$', RegistrationView.as_view(), name = 'Registration View'),
    url(r'^company$', CompanyListView.as_view(), name = 'Company List View'),
    url(r'^company/(?P<company_id>[0-9]+)$', CompanyDetailView.as_view(), name = 'Company Detail View'),
    url(r'^user$', UserListView.as_view(), name = 'User List View'),
    url(r'^user/(?P<user_id>[0-9]+)$', UserDetailView.as_view(), name = 'User Detail View'),
    url(r'^upload$', UploadItemView.as_view(), name ='app_upload_item')
]
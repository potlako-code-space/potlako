"""potlako URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls.conf import path, include
from django.views.generic.base import RedirectView

from edc_action_item.admin_site import edc_action_item_admin
from edc_appointment.admin_site import edc_appointment_admin
from edc_identifier.admin_site import edc_identifier_admin
from edc_lab.admin_site import edc_lab_admin
from edc_locator.admin_site import edc_locator_admin
from edc_metadata.admin_site import edc_metadata_admin
from edc_reference.admin_site import edc_reference_admin
from edc_registration.admin_site import edc_registration_admin
from edc_visit_schedule.admin_site import edc_visit_schedule_admin

from potlako_subject.admin_site import potlako_subject_admin
from potlako_prn.admin_site import potlako_prn_admin
from .views import HomeView, AdministrationView


urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', admin.site.urls),
    path('admin/', potlako_subject_admin.urls),
    path('admin/', potlako_prn_admin.urls),
    path('admin/', edc_appointment_admin.urls),
    path('admin/', edc_lab_admin.urls),
    path('admin/', edc_locator_admin.urls),
    path('admin/', edc_identifier_admin.urls),
    path('admin/', edc_metadata_admin.urls),
    path('admin/', edc_registration_admin.urls),
    path('admin/', edc_reference_admin.urls),
    path('admin/', edc_action_item_admin.urls),
    path('admin/edc_visit_schedule/', edc_visit_schedule_admin.urls),

    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('admin/potlako_subject/',
         RedirectView.as_view(url='admin/potlako_subject/'),
         name='potlako_subject_models_url'),

    path('appointment/', include('edc_appointment.urls')),
    path('edc_action_item/', include('edc_action_item.urls')),
    path('edc_base/', include('edc_base.urls')),
    path('edc_consent/', include('edc_consent.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_locator/', include('edc_locator.urls')),
    path('edc_metadata/', include('edc_metadata.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('edc_identifier/', include('edc_identifier.urls')),
    path('edc_reference/', include('edc_reference.urls')),
    path('edc_registration/', include('edc_registration.urls')),
    path('edc_subject_dashboard/', include('edc_subject_dashboard.urls')),

    #     path('edc_sync/', include('edc_sync.urls')),
    #     path('edc_sync_files/', include('edc_sync_files.urls')),

    path('edc_visit_schedule/', include('edc_visit_schedule.urls')),
    path('potlako_subject/', include('potlako_subject.urls')),
    path('potlako_prn/', include('potlako_prn.urls')),
    path('subject/', include('potlako_dashboard.urls')),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
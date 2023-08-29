import configparser
import os
from datetime import datetime

from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.management.color import color_style
from edc_appointment.appointment_config import AppointmentConfig
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_data_manager.apps import AppConfig as BaseEdcDataManagerAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
from edc_sms.apps import AppConfig as BaseEdcSmsAppConfig
from edc_sync.apps import AppConfig as BaseEdcSyncAppConfig
from edc_sync_files.apps import AppConfig as BaseEdcSyncFilesAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from potlako_dashboard.patterns import subject_identifier

style = color_style()

config = configparser.RawConfigParser()
config.read(os.path.join(settings.ETC_DIR,
                         settings.CONFIG_FILE))


class AppConfig(DjangoAppConfig):
    name = 'potlako'


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    send_sms_reminders = True
    apply_community_filter = True
    configurations = [
        AppointmentConfig(
            model='edc_appointment.appointment',
            related_visit_model='potlako_subject.subjectvisit',
            appt_type='clinic')]


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP132'
    protocol_name = 'Potlako Plus'
    protocol_number = '132'
    protocol_title = ''
    study_open_datetime = datetime(
        2020, 3, 1, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(
        2025, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Potlako Plus'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '132'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'potlako_subject': ('subject_visit', 'potlako_subject.subjectvisit')
        }


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = 'botswana'
    definitions = {
        '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[100, 100, 100, 100, 100, 100, 100]),
        '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                             slots=[100, 100, 100, 100, 100])
        }


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'potlako_subject.subjectvisit': 'reason'}
    other_visit_reasons = ['off study', 'deferred', 'death']
    other_create_visit_reasons = [
        'initial_visit/contact', 'fu_visit/contact',
        'unscheduled_visit/contact', 'missed_visit']
    create_on_reasons = [SCHEDULED, UNSCHEDULED] + other_create_visit_reasons
    delete_on_reasons = [LOST_VISIT] + other_visit_reasons


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    use_settings = True
    device_id = settings.DEVICE_ID
    device_role = settings.DEVICE_ROLE


class EdcDataManagerAppConfig(BaseEdcDataManagerAppConfig):
    identifier_pattern = subject_identifier


class EdcSmsAppConfig(BaseEdcSmsAppConfig):
    locator_model = 'potlako_subject.subjectlocator'
    consent_model = 'potlako_subject.subjectconsent'
    sms_model = 'potlako_subject.sms'


class EdcSyncAppConfig(BaseEdcSyncAppConfig):
    edc_sync_files_using = True
    server_ip = os.getenv('EDC_SYNC_SERVER_IP')
    base_template_name = 'potlako/base.html'
    update_models = True


class EdcSyncFilesAppConfig(BaseEdcSyncFilesAppConfig):
    edc_sync_files_using = True
    remote_host = os.getenv('EDC_SYNC_FILES_REMOTE_HOST')
    user = os.getenv('EDC_SYNC_FILES_SYNC_USER')
    usb_volume = os.getenv('EDC_SYNC_FILES_USB_VOLUME')
    remote_media = os.getenv('EDC_SYNC_FILES_REMOTE_MEDIA')
    tmp_folder = os.path.join(settings.MEDIA_ROOT, 'transactions', 'tmp')
    incoming_folder = os.path.join(settings.MEDIA_ROOT, 'transactions', 'incoming')
    media_path = os.path.join(settings.MEDIA_ROOT, 'verbal_consents')
    media_dst = os.path.join(settings.MEDIA_ROOT, 'verbal_consents')
    media_tmp = os.path.join('/tmp/')

    def make_required_folders(self):
        """Makes all folders declared in the config if they
        do not exist.
        """
        client_folders = [self.outgoing_folder, self.archive_folder]

        server_folders = [self.incoming_folder, self.archive_folder,
                          self.tmp_folder, self.pending_folder,
                          self.log_folder]

        folder_dict = {'Client': client_folders,
                       'CentralServer': server_folders
                       }
        role = os.getenv('EDC_DEVICE_ROLE')

        for folder in folder_dict.get(role):
            if not os.path.exists(folder):
                os.makedirs(folder)

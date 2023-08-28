from datetime import datetime, timedelta
from django.apps import apps as django_apps
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'potlako/home.html'
    navbar_name = 'potlako'
    navbar_selected_item = 'home'

    clinician_call_enrollment_model = 'potlako_subject.cliniciancallenrollment'
    subject_screening_model = 'potlako_subject.subjectscreening'
    subject_consent_model = 'potlako_subject.subjectconsent'

    @property
    def clinician_call_enrollment_cls(self):
        return django_apps.get_model(self.clinician_call_enrollment_model)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollments = self.clinician_call_enrollment_cls.objects.all()
        subject_screenig = self.subject_screening_cls.objects.all()
        subject_consent = self.subject_consent_cls.objects.all()

        past_week = self.clinician_call_enrollment_cls.objects.filter(
                    created__gte=datetime.now() - timedelta(days=7)).count()

        enhanced_care = ['otse_clinic', 'mmankgodi_clinic',
                         'letlhakeng_clinic',
                         'mathangwane clinic', 'ramokgonami_clinic',
                         'sefophe_clinic',
                         'mmadinare_primary_hospital', 'tati_siding_clinic',
                         'bokaa_clinic', 'masunga_primary_hospital',
                         'masunga_clinic',
                         'mathangwane_clinic', 'manga_clinic']
        intervention = ['mmathethe_clinic', 'molapowabojang_clinic',
                        'lentsweletau_clinic', 'oodi_clinic',
                        'metsimotlhabe_clinic',
                        'shoshong_clinic', 'lerala_clinic',
                        'maunatlala_clinic',
                        'nata_clinic', 'mandunyane_clinic',
                        'sheleketla_clinic']

        intervention_enrolled = self.clinician_call_enrollment_cls.objects.\
            filter(facility__in=intervention).count()
        enhanced_care_enrolled = self.clinician_call_enrollment_cls.objects. \
            filter(facility__in=enhanced_care).count()

        enrolled_subjects = enrollments.count()
        screened_subjects = subject_screenig.count()
        consented_subjects = subject_consent.count()

        context.update(
            enhanced_care_enrolled=enhanced_care_enrolled,
            intervention_enrolled=intervention_enrolled,
            consented_subjects=consented_subjects,
            enrolled_subjects=enrolled_subjects,
            past_week=past_week,
            screened_subjects=screened_subjects)

        return context

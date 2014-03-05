from celery.task import task
from ashtag.apps.core.models import EmailTemplate
from ashtag.apps.export.datacollections import SurveyCollection, SightingCollection, UserCollection
from ashtag.apps.export.dataformatters import CsvFormatter
from ashtag.apps.export.datawriters import FileWriter


@task()
def send_export_emails():
    survey_writer = FileWriter(CsvFormatter(SurveyCollection()), name='surveys')
    sighting_writer = FileWriter(CsvFormatter(SightingCollection()), name='sightings')
    user_writer = FileWriter(CsvFormatter(UserCollection()), name='users')

    with survey_writer as survey_file, sighting_writer as sighting_file, user_writer as user_file:
        sylva_email_template = EmailTemplate.objects.get(name='export_sylva_foundation')
        sylva_email = sylva_email_template.make_email()
        sylva_email.attach_file(survey_file.name)
        sylva_email.attach_file(sighting_file.name)

        internal_email_template = EmailTemplate.objects.get(name='export_internal')
        internal_email = internal_email_template.make_email()
        internal_email.attach_file(survey_file.name)
        internal_email.attach_file(sighting_file.name)
        internal_email.attach_file(user_file.name)

        sylva_email.send()
        internal_email.send()


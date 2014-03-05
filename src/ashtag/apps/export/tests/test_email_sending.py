from django.core import mail
from django.test import TestCase
from ashtag.apps.export.tasks import send_export_emails


class EmailSendingTestCase(TestCase):
    fixtures = ['email-templates']
    
    def test_sent(self):
        send_export_emails()

        partner_email = mail.outbox[0]
        attachments_file_names = [m[0] for m in partner_email.attachments]
        self.assertTrue(attachments_file_names[0].startswith('surveys.'), attachments_file_names[0])
        self.assertTrue(attachments_file_names[0].endswith('.csv.zip'), attachments_file_names[0])
        self.assertTrue(attachments_file_names[1].startswith('sightings.'), attachments_file_names[1])
        self.assertTrue(attachments_file_names[1].endswith('.csv.zip'), attachments_file_names[1])

        internal_email = mail.outbox[1]
        attachments_file_names = [m[0] for m in internal_email.attachments]
        self.assertTrue(attachments_file_names[0].startswith('surveys.'), attachments_file_names[0])
        self.assertTrue(attachments_file_names[0].endswith('.csv.zip'), attachments_file_names[0])
        self.assertTrue(attachments_file_names[1].startswith('sightings.'), attachments_file_names[1])
        self.assertTrue(attachments_file_names[1].endswith('.csv.zip'), attachments_file_names[1])
        self.assertTrue(attachments_file_names[2].startswith('users.'), attachments_file_names[2])
        self.assertTrue(attachments_file_names[2].endswith('.csv.zip'), attachments_file_names[2])
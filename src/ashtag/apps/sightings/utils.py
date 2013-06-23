#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings


def email_owner(tree, subject, message, fail_silently=True):
    """Send emails to tree owner."""
    send_mail(
        "[AshTag] {0}".format(subject),
        message,
        settings.DEFAULT_FROM_EMAIL,
        [tree.creator_email],
        fail_silently=fail_silently)

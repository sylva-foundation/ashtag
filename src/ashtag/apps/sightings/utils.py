#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.mail import send_mail


def email_owner(tree, subject, message, fail_silently=True):
    """Send emails to tree owner."""
    send_mail(
        "[AshTag] {0}".format(subject),
        message,
        [tree.creator_email],
        fail_silently=fail_silently)

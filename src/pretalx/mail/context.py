from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from pretalx.common.urls import build_absolute_uri


def get_context_explanation():
    return [
        {
            'name': 'confirmation_link',
            'explanation': _('Link to confirm a submission after it has been accepted.'),
        },
        {
            'name': 'event_name',
            'explanation': _('The event\'s full name.'),
        },
        {
            'name': 'submission_title',
            'explanation': _('The title of the submission in question. Only usable in default templates.'),
        },
        {
            'name': 'submission_url',
            'explanation': _('The link to a submission. Only usable in default templates.'),
        },
        {
            'name': 'speakers',
            'explanation': _('The name(s) of all speakers in this submissoin.'),
        },
    ]


def template_context_from_event(event):
    return {
        'all_submissions_url': build_absolute_uri(
            'cfp:event.user.submissions',
            kwargs={'event': event.slug}
        ),
    }


def template_context_from_submission(submission):
    ctx = template_context_from_event(submission.event)
    ctx.update({
        'confirmation_link': build_absolute_uri(
            'cfp:event.user.submission.confirm',
            kwargs={'event': submission.event.slug, 'code': submission.code}
        ),
        'event_name': submission.event.name,
        'submission_title': submission.title,
        'submission_url': submission.urls.user_base.full(scheme='https', hostname=settings.SITE_NETLOC),
        'speakers': submission.display_speaker_names,
        'orga_url': submission.orga_urls.base.full(scheme='https', hostname=settings.SITE_NETLOC),
    })
    return ctx

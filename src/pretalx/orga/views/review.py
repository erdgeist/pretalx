from django.contrib import messages
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from pretalx.common.views import ActionFromUrl, CreateOrUpdateView
from pretalx.orga.forms import ReviewForm
from pretalx.person.models import EventPermission
from pretalx.submission.models import Review


class ReviewContext():

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        submission = self.request.event.submissions.get(code=self.kwargs['code'])
        ctx['submission'] = submission
        ctx['review'] = submission.reviews.filter(user=self.request.user).first()
        return ctx


class ReviewDashboard(ListView):
    template_name = 'orga/review/dashboard.html'
    paginate_by = 25
    context_object_name = 'submissions'

    def get_queryset(self, *args, **kwargs):
        return self.request.event.submissions\
            .annotate(avg_score=models.Avg('reviews__score'))\
            .order_by('-avg_score')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['missing_reviews'] = Review.find_missing_reviews(self.request.event, self.request.user)
        ctx['reviewers'] = EventPermission.objects.filter(is_reviewer=True, event=self.request.event).count()
        ctx['next_submission'] = Review.find_missing_reviews(self.request.event, self.request.user).first()
        return ctx


class ReviewSubmission(ReviewContext, ActionFromUrl, CreateOrUpdateView):

    form_class = ReviewForm
    model = Review
    template_name = 'orga/submission/review.html'

    @property
    def submission(self):
        return self.request.event.submissions.get(code__iexact=self.kwargs['code'])

    def get_object(self):
        return self.submission.reviews.exclude(user__in=self.submission.speakers.all()).filter(user=self.request.user).first()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.request.event
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.submission = self.submission
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:

        if self.request.POST.get('show_next', '0').strip() == '1':
            next_submission = Review.find_missing_reviews(self.request.event, self.request.user).first()
            if next_submission:
                messages.success(self.request, _('You are on a roll!'))  # TODO: choose from a list of messages
                return next_submission.orga_urls.new_review
            else:
                messages.success(self.request, _('Nice, you have no submissions left to review!'))
                return self.request.event.orga_urls.reviews

        return self.submission.orga_urls.reviews


class ReviewSubmissionDelete(ReviewContext, TemplateView):
    template_name = 'orga/review/submission_delete.html'

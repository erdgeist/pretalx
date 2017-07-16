from datetime import timedelta

from django.views.generic import TemplateView, View


class ScheduleView(TemplateView):
    template_name = 'agenda/schedule.html'

    def get_object(self):
        if self.request.GET.get('version'):
            return self.request.event.schedules.filter(version=self.request.GET.get('version'))
        return self.request.event.current_schedule

    def get_context_data(self, event):
        ctx = super().get_context_data()
        schedule = self.get_object()

        if not schedule and self.request.GET.get('version'):
            ctx['version'] = self.request.GET.get('version')
            ctx['error'] = 'wrong-version'
            return ctx
        elif not schedule:
            ctx['error'] = 'no-schedule'
            return ctx
        ctx['schedule'] = schedule
        ctx['schedules'] = self.request.event.schedules.filter(published__isnull=False).values_list('version')
        return ctx


class FrabView(ScheduleView):
    template_name = 'agenda/schedule.xml'

    def get_context_data(self, event):
        ctx = super().get_context_data(event)
        event = self.request.event
        schedule = ctx.get('schedule')
        if not schedule:
            return ctx

        ctx['data'] = [
            {
                'index': index + 1,
                'start': current_date,
                'end': current_date + timedelta(days=1),
                'rooms': [{
                    'name': room.name,
                    'talks': [talk for talk in schedule.talks.filter(start__date=current_date.date(), room=room)],
                } for room in event.rooms.all()],
            } for index, current_date in enumerate([
                event.datetime_from + timedelta(days=i) for i in range((event.date_to - event.date_from).days + 1)
            ])
        ]
        return ctx


class TalkView(View):
    pass
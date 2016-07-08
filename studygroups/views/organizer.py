import datetime

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib import messages
from django.conf import settings
from django import http
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from studygroups.models import Course
from studygroups.models import StudyGroup
from studygroups.models import TeamMembership
from studygroups.models import Facilitator
from studygroups.models import StudyGroupMeeting
from studygroups.models import report_data
from studygroups.models import generate_all_meetings
from studygroups.models import get_team_users
from studygroups.forms import StudyGroupForm
from studygroups.decorators import user_is_organizer


@user_is_organizer
def organize(request):
    # TODO 
    # - Only show learning circles with meetings in the future
    # - Only show meetings for current week 
    today = datetime.datetime.now().date()
    two_weeks_ago = today - datetime.timedelta(weeks=2, days=today.weekday())
    two_weeks = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(weeks=3)
    study_groups = StudyGroup.objects.active()
    facilitators = Facilitator.objects.all()    

    if not request.user.is_staff:
        team_users = get_team_users(request.user)
        study_groups = study_groups.filter(facilitator__in=team_users)
        facilitators = facilitators.filter(user__in=team_users)

    context = {
        'courses': Course.objects.all(),
        'study_groups': study_groups,
        'meetings': StudyGroupMeeting.objects.active().filter(study_group__in=StudyGroup.objects.active(), meeting_date__gte=two_weeks_ago).exclude(meeting_date__gte=two_weeks),
        'facilitators': facilitators,
        'today': timezone.now(),
    }
    return render_to_response('studygroups/organize.html', context, context_instance=RequestContext(request))


class CourseUpdate(UpdateView):
    model = Course
    fields = [    
        'title',
        'provider',
        'link',
        'start_date',
        'duration',
        'prerequisite',
        'time_required',
        'caption',
    ]
    success_url = reverse_lazy('studygroups_organize')


class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('studygroups_organize')
    template_name = 'studygroups/confirm_delete.html'


class StudyGroupCreate(CreateView):
    model = StudyGroup
    form_class = StudyGroupForm
    success_url = reverse_lazy('studygroups_organize')

    def form_valid(self, form):
        self.object = form.save()
        generate_all_meetings(self.object)
        return http.HttpResponseRedirect(self.get_success_url())


@user_is_organizer
def report(request):
    # TODO - remove this view
    study_groups = StudyGroup.objects.active()
    for study_group in study_groups:
        study_group.laptop_stats = {}
    context = {
        'study_groups': study_groups,
    }
    return render_to_response('studygroups/report.html', context, context_instance=RequestContext(request))


@user_is_organizer
def weekly_report(request, year=None, month=None, day=None ):
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if month and day and year:
        today = today.replace(year=int(year), month=int(month), day=int(day))
    start_time = today - datetime.timedelta(days=today.weekday())
    end_time = start_time + datetime.timedelta(days=7)
    context = {
        'start_time': start_time,
        'end_time': end_time,
    }
    # get team for current user
    team = None
    membership = TeamMembership.objects.filter(user=request.user, role=TeamMembership.ORGANIZER).first()
    if membership:
        team = membership.team

    context.update(report_data(start_time, end_time, team))
    return render_to_response('studygroups/weekly-update.html', context, context_instance=RequestContext(request))


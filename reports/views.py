import json

import persian
import urllib

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from khayyam import JalaliDatetime
from rest_framework import permissions, mixins
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet

from reports.forms import ReportForm
from reports.models import Report
from reports.serializers import GroupSerializer, UserSerializer, ReportSerializer
from reports.utils import unique_reference_number, utc_to_local
from whistleblowers import settings


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def thanks(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        a = Report.objects.first()
        mm = utc_to_local(a.modified_datetime)
        currenct = JalaliDatetime(mm)
        return render(request, 'thanks.html', {'created_datetime': currenct.strftime("%C"), 'ref_number': "۱۲۳۴۵۶۷۸۹۲"})

    # if a GET (or any other method) we'll create a blank form


def home(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        return render(request, 'home.html', )

    # if a GET (or any other method) we'll create a blank form


def new_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                reference_number = unique_reference_number()
                new_report = form.save(commit=False)
                new_report.reference_number = reference_number
                new_report.save()
                ref_number = persian.convert_en_numbers(str(reference_number))
                created_datetime = utc_to_local(new_report.created_datetime)
                created_datetime = JalaliDatetime(created_datetime)
                return render(request, 'thanks.html',
                              {'ref_number': ref_number,
                               'created_datetime': created_datetime.strftime('%C')})
            else:
                messages.error(request, 'reCAPTCHA نامعتبر است. لطفا دوباره تلاش کنید.')


    else:
        form = ReportForm()
    return render(request, 'new_report.html', {'form': form})


# class ReportViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = ReportSerializer
#     queryset = Report.objects.all()
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'reports.html'
#
#     def form(self, request, *args, **kwargs):
#         serializer = self.get_serializer()
#         renderer = HTMLFormRenderer()
#         form_html = renderer.render(serializer.data, renderer_context={
#             'template': 'rest_framework/api_form.html',
#             'request': request
#         })
#         return HttpResponse(form_html)
#
#     def get(self, request):
#         content = {'serializer': ReportSerializer}
#         return Response(content)

class ReportViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,

                    GenericViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    model = Report
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

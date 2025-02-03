import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView
import zipfile
from email.parser import Parser
from django.shortcuts import render
from django.views import View

from .forms import WheelUploadForm
from .models import Wheel
from users.mixins import LoggedInOnlyView

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class CurrentTimeClassView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        template_path = 'index.html'
        now = datetime.datetime.now()
        return render(request, template_path, {'time': now})


class UTCClassView(LoggedInOnlyView, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(UTCClassView, self).get_context_data(**kwargs)
        utc_now = datetime.datetime.now(datetime.UTC)
        context.update(
            {
                'time': utc_now,
            }
        )
        return context

import zipfile
from email.parser import Parser
from django.shortcuts import render
from django.views import View
from .forms import WheelUploadForm
from .models import Wheel

class UploadWheelView(View):
    def get(self, request):
        form = WheelUploadForm()
        return render(request, 'upload_wheel.html', {'form': form, 'wheel': None, 'file_url': None})

    def post(self, request):
        form = WheelUploadForm(request.POST, request.FILES)
        wheel_instance = None
        file_url = None
        if form.is_valid():
            wheel_instance = form.save(commit=False)
            file = request.FILES['file_path']

            # 파싱 로직: .whl 파일에서 메타데이터 추출
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file, 'r') as z:
                    for filename in z.namelist():
                        if filename.endswith('METADATA'):
                            with z.open(filename) as metadata_file:
                                metadata_content = metadata_file.read().decode('utf-8')
                                metadata = Parser().parsestr(metadata_content)
                                wheel_instance.name = metadata.get('Name', 'Unknown')
                                wheel_instance.version = metadata.get('Version', 'Unknown')
                                wheel_instance.summary = metadata.get('Summary', 'No summary available')
                                wheel_instance.author = metadata.get('Author', 'Unknown')
                                wheel_instance.license = metadata.get('License', 'Unknown')
                            break

            # 데이터베이스에 저장
            wheel_instance.save()

            # 업로드된 파일의 URL 가져오기
            file_url = wheel_instance.file_path.url
        else:
            form.add_error(None, 'Invalid file format. Please upload a valid .whl file.')

        return render(request, 'upload_wheel.html', {'form': form, 'wheel': wheel_instance, 'file_url': file_url})


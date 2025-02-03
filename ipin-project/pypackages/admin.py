import zipfile
from email.parser import Parser
from django.contrib import admin
from django.utils.html import format_html
from .models import Wheel
from django.utils.timezone import now

@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'author', 'summary', 'license', 'keywords', 'created_at', 'download_link')
    list_display_links = ('name', 'version', 'created_at')  # 클릭 가능 영역 확장
    readonly_fields = ('name', 'version', 'author', 'summary', 'license', 'keywords', 'description')

    def save_model(self, request, obj, form, change):
        if obj.file_path:
            # Django FileField 객체 처리
            uploaded_file = obj.file_path.file

            try:
                if zipfile.is_zipfile(uploaded_file):
                    with zipfile.ZipFile(uploaded_file, 'r') as z:
                        metadata_file = next((f for f in z.namelist() if f.endswith('METADATA')), None)
                        if metadata_file:
                            with z.open(metadata_file) as metadata:
                                metadata_content = metadata.read().decode('utf-8')
                                parsed_metadata = Parser().parsestr(metadata_content)

                                # 목록 필드에 데이터 저장
                                obj.name = parsed_metadata.get('Name', 'Unknown')[:20]
                                obj.version = parsed_metadata.get('Version', 'Unknown')[:20]
                                obj.summary = parsed_metadata.get('Summary', 'Not available')
                                obj.author = parsed_metadata.get('Author', 'Not available')[:100]
                                obj.license = parsed_metadata.get('License', 'Not available')[:50]
                                obj.keywords = parsed_metadata.get('Keywords', 'Not available')
                                obj.description = parsed_metadata.get('Description', 'Not available')
            except Exception as e:
                print(f"Error processing the uploaded file: {e}")

        if not obj.created_at:
            obj.created_at = now()

        super().save_model(request, obj, form, change)

    def download_link(self, obj):
        if obj.file_path and obj.file_path.url:
            return format_html('<a href="{}" download>Download</a>', obj.file_path.url)
        return "No file"

    download_link.short_description = "Download"


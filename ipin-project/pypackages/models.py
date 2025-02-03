import datetime
from django.db import models

class Wheel(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField( max_length=20)
    file_path = models.FileField(upload_to='upload/', blank=True, null=True)
    #author = models.ForeignKey(WatchData,on_delete=models.CASCADE,)
    created_at = models.DateTimeField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)  # 간단한 설명
    author = models.CharField(max_length=100, blank=True, null=True)  # 작성자 이름
    license = models.CharField(max_length=50, blank=True, null=True)  # 라이선스 정보
    keywords = models.TextField(blank=True, null=True)  # 키워드 (쉬버 구분)
    description = models.TextField(blank=True, null=True)  # 상세 설명

    def __str__(self):
        return f"{self.name} - {self.version}"

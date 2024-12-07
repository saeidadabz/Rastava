from django.db import models

from django.db import models

class Contract(models.Model):
    title = models.CharField(max_length=255)  # عنوان قرارداد
    recipient_email = models.EmailField()  # ایمیل گیرنده
    envelope_id = models.CharField(max_length=255, blank=True, null=True)  # Envelope ID
    status = models.CharField(max_length=50, default="created")  # وضعیت قرارداد
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد قرارداد
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ آخرین به‌روزرسانی
    document = models.FileField(upload_to='contracts/')  # فایل قرارداد

    def __str__(self):
        return self.title


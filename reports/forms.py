from django import forms
from reports.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ['created_datetime', 'reference_number']
        labels = {
            "reporter_name": "نام گزارش دهنده (اختیاری)",
            "title": "شرح فساد رو خلاصه و دقیق با زمان و مکانش اینجا زیر بنویس👇",
            "description": "توضیحات گزارش",
            "document": "اگر مدرک یا فایل مرتبطی داری اینجا آپلود کن",
            "phone_number": "تلفن همراه (اختیاری)",
        }

        # widgets = {
        #     # 'first_name': forms.TextInput(attrs={'placeholder': 'اسم خودت'}),
        #     'description': forms.Textarea(
        #         attrs={'placeholder': 'شرح فساد رو خلاصه و دقیق با زمان و مکانش اینجا بنویس.'}),
        # }

from django.contrib import admin
from .models import FAQ, CompanyInfo, Internship, Role, Student, PlacementRecord, QuickInfo,PolicyFAQ

admin.site.register(FAQ)
admin.site.register(CompanyInfo)
admin.site.register(Student)
admin.site.register(PlacementRecord)
admin.site.register(QuickInfo)
admin.site.register(Role)
admin.site.register(Internship)
admin.site.register(PolicyFAQ)
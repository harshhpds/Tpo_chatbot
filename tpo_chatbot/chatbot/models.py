from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    contact_email = models.EmailField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name

class Role(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='roles')
    role_title = models.CharField(max_length=100)
    role_description = models.TextField()
    salary_package = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    eligibility = models.TextField(null=True, blank=True)
    application_form_link = models.URLField(null=True, blank=True)
    hr_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.role_title} at {self.company.company_name}"
    

class Internship(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='internships')
    internship_title = models.CharField(max_length=100)
    internship_description = models.TextField()
    stipend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)  # e.g., "3 months"
    location = models.CharField(max_length=100, null=True, blank=True)
    eligibility = models.TextField(null=True, blank=True)
    application_form_link = models.URLField(null=True, blank=True)
    mentor_contact = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.internship_title} at {self.company.company_name}"

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    year_of_study = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.branch})"

class PlacementRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    package = models.DecimalField(max_digits=10, decimal_places=2)
    placement_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} placed in {self.company.company_name} with {self.package} LPA"

class QuickInfo(models.Model):
    info_key = models.CharField(max_length=100, unique=True)
    info_value = models.TextField()

    def __str__(self):
        return self.info_key

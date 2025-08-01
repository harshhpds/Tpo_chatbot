from django.db import models
from django.contrib.auth.models import AbstractUser

class FAQ(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    website = models.TextField(null=True, blank=True)
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

class PlacementStatistics(models.Model):
    branch = models.CharField(max_length=50)  # E.g., "B.Tech Civil"
    enrolled_to_tpo = models.IntegerField()  # Number of students enrolled
    total_placed = models.IntegerField()  # Total students placed
    placement_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Placement percentage
    average_ctc = models.DecimalField(max_digits=10, decimal_places=2)  # Average CTC in LPA
    academic_year = models.CharField(max_length=9,null=True )  # E.g., "2022-2023"

    def __str__(self):
        return f"{self.branch} - {self.placement_percentage}% Placement ({self.academic_year})"

class TopCompanyOffers(models.Model):
    company_name = models.CharField(max_length=100)
    ctc_in_lakhs = models.DecimalField(max_digits=10, decimal_places=2)
    branch = models.CharField(max_length=50, null=True, blank=True)  # For specific branches or general offers
    academic_year = models.CharField(max_length=9)  # E.g., "2022-2023"

    def __str__(self):
        return f"{self.company_name} - {self.ctc_in_lakhs} LPA ({self.academic_year})"

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('tpo', 'TPO Officer'),
        ('student', 'Student'),
        ('company', 'Company'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    # Override groups and user_permissions to avoid reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Policy(models.Model):
    POLICY_TYPES = [
        ('Placement', 'Placement'),
        ('Internship', 'Internship'),
        ('General', 'General'),
        # Add more policy types as needed
    ]

    policy_type = models.CharField(max_length=50, choices=POLICY_TYPES)
    policy_title = models.CharField(max_length=255)
    policy_text = models.TextField()

    def __str__(self):
        return f"{self.policy_type} - {self.policy_title}"

class PolicyFAQ(models.Model):
    category = models.CharField(max_length=100, null=True)  # e.g., Placement, Internship, Code of Conduct
    question = models.TextField()               # The question or intent
    keywords = models.TextField(default="default")               # Comma-separated keywords for better searchability
    answer = models.TextField()
    embedding = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.question
    


class PolicyFAQ2(models.Model):
    POLICY_TYPES = [
        ('Placement', 'Placement'),
        ('Internship', 'Internship'),
        ('Code of Conduct', 'Code of Conduct'),
        ('General', 'General'),
    ]

    APPLICABLE_TO_CHOICES = [
        ('BTech', 'BTech'),
        ('MTech', 'MTech'),
        ('MCA', 'MCA'),
        ('All', 'All'),
    ]

    # Core fields
    category = models.CharField(max_length=100, null=True, blank=True)  # e.g., Placement, Internship, Code of Conduct
    question = models.TextField()  # The question or intent
    answer = models.TextField()  # The detailed answer
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPES, default='General')  # Type of policy
    academic_year = models.CharField(max_length=9, null=True, blank=True)  # E.g., "2023-2024"
    source = models.CharField(max_length=255, null=True, blank=True)  # Source of the policy (e.g., PDF name)

    # Metadata for better searchability
    applicable_to = models.CharField(max_length=50, choices=APPLICABLE_TO_CHOICES, default='All')  # Who the policy applies to
    related_policy = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Link to related policies

    def __str__(self):
        return f"{self.question} ({self.policy_type})"



class Document(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)  # e.g., "company_list", "policy", etc.
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

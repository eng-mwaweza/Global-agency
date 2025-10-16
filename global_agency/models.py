from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True,  null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"

class StudentApplication(models.Model):
    # Step 1: Personal Information
    full_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    nationality = models.CharField(max_length=100, default="Tanzanian")
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.TextField()

    # Step 2: Parents Details
    father_name = models.CharField(max_length=150, blank=True, null=True)
    father_phone = models.CharField(max_length=50, blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)
    father_occupation = models.CharField(max_length=150, blank=True, null=True)

    mother_name = models.CharField(max_length=150, blank=True, null=True)
    mother_phone = models.CharField(max_length=50, blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)
    mother_occupation = models.CharField(max_length=150, blank=True, null=True)

    # Step 3: Education Background - O-Level
    olevel_school = models.CharField(max_length=150, blank=True, null=True)
    olevel_country = models.CharField(max_length=100, default="Tanzania")
    olevel_address = models.CharField(max_length=255, blank=True, null=True)
    olevel_region = models.CharField(max_length=100, blank=True, null=True)
    olevel_year = models.CharField(max_length=10, blank=True, null=True)
    olevel_candidate_no = models.CharField(max_length=50, blank=True, null=True)
    olevel_gpa = models.CharField(max_length=20, blank=True, null=True)

    # Step 3: Education Background - A-Level
    alevel_school = models.CharField(max_length=150, blank=True, null=True)
    alevel_country = models.CharField(max_length=100, default="Tanzania")
    alevel_address = models.CharField(max_length=255, blank=True, null=True)
    alevel_region = models.CharField(max_length=100, blank=True, null=True)
    alevel_year = models.CharField(max_length=10, blank=True, null=True)
    alevel_candidate_no = models.CharField(max_length=50, blank=True, null=True)
    alevel_gpa = models.CharField(max_length=20, blank=True, null=True)

    # Step 4: Study Preferences
    preferred_country_1 = models.CharField(max_length=100, blank=True, null=True)
    preferred_country_2 = models.CharField(max_length=100, blank=True, null=True)
    preferred_country_3 = models.CharField(max_length=100, blank=True, null=True)
    preferred_country_4 = models.CharField(max_length=100, blank=True, null=True)
    preferred_program_1 = models.CharField(max_length=100, blank=True, null=True)
    preferred_program_2 = models.CharField(max_length=100, blank=True, null=True)
    preferred_program_3 = models.CharField(max_length=100, blank=True, null=True)
    preferred_program_4 = models.CharField(max_length=100, blank=True, null=True)

    # Step 5: Emergency Contact
    emergency_name = models.CharField(max_length=150)
    emergency_address = models.TextField()
    emergency_occupation = models.CharField(max_length=100, blank=True, null=True)
    emergency_gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    emergency_relation = models.CharField(max_length=100)
    heard_about_us = models.CharField(max_length=100, blank=True, null=True)
    heard_about_other = models.CharField(max_length=255, blank=True, null=True)

    # System fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.nationality})"


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic Info
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    # Social Links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    # Resume
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    # Target Info
    target_domain = models.CharField(max_length=100, blank=True)
    target_company = models.CharField(max_length=100, blank=True)

    # Extra
    bio = models.TextField(blank=True)

    # Activity Fields (for later phases)
    last_login_date = models.DateField(blank=True, null=True)
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    


class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'login_date')

    def __str__(self):
        return f"{self.user.username} - {self.login_date}"
    

class PlacementProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Progress fields (percentage)
    dsa_progress = models.IntegerField(default=0)
    aptitude_progress = models.IntegerField(default=0)
    core_subjects_progress = models.IntegerField(default=0)
    interview_prep_progress = models.IntegerField(default=0)

    def overall_progress(self):
        return int(
            (self.dsa_progress +
             self.aptitude_progress +
             self.core_subjects_progress +
             self.interview_prep_progress) / 4
        )

    def __str__(self):
        return self.user.username
    

class PracticeQuestion(models.Model):

    QUESTION_TYPES = [
        ('aptitude', 'Aptitude'),
        ('coding', 'Coding'),
        ('interview', 'Interview'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    domain = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES
    )

    page_number = models.IntegerField(default=1)  # 🔥 pagination support

    question_text = models.TextField()

    answer = models.TextField(blank=True, null=True)  # For interview
    leetcode_link = models.URLField(blank=True, null=True)  # For coding

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question_type} - Page {self.page_number}"
    

class Roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.domain} - {self.company}"
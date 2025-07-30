from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    name = models.CharField(max_length=100)         # e.g. Fresher, Internship
    duration = models.CharField(max_length=50)      # e.g. 0–1 years

    def __str__(self):
        return f"{self.name} ({self.duration})"


class JobVacancy(models.Model):
    post_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    job_description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)  # For multiple lines
    required_skills = models.TextField(blank=True, null=True)


    def skill_list(self):
        return [skill.strip() for skill in self.required_skills.split(',')]

    def __str__(self):
        return self.post_name




class Statistic(models.Model):
    title = models.CharField(max_length=100)  
    count = models.PositiveIntegerField()     

    def __str__(self):
        return self.title
    



class JobApplication(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} applied for {self.position}"
    

class Blog(models.Model):
    keyword = models.CharField(max_length=100)
    date = models.DateField()
    short_heading = models.CharField(max_length=150, help_text="Heading for card display")
    full_heading = models.CharField(max_length=250, help_text="Full heading for modal display")
    paragraph1 = models.TextField()
    paragraph2 = models.TextField(blank=True, null=True)
    paragraph3 = models.TextField(blank=True, null=True)
    paragraph4 = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blogs/')

    def __str__(self):
        return self.short_heading



class ClientLogo(models.Model):
    image = models.ImageField(upload_to='client_logos/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.alt_text or f"Client Logo {self.id}"
    




class LifeEvent(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField(default="No description")
    para1 = models.TextField(blank=True, null=True)
    para2 = models.TextField(blank=True, null=True)
    para3 = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, default="Anniversary")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.heading

class LifeEventImage(models.Model):
    event = models.ForeignKey(LifeEvent, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='life_events/')

    def __str__(self):
        return f"{self.event.heading} - Image"



class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
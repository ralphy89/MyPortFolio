from DateTime import DateTime
from django.db import models
from multiselectfield import MultiSelectField


# Create your models here.


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=500)
    degree = models.CharField(max_length=100)
    about = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    title_description = models.TextField(max_length=500)
    title_description_1 = models.TextField(max_length=500)

    skills = list()

    def get_skills(self):
        return self.skills

    def set_skills(self, sk):
        self.skills = sk

    def get_n_skill(self):
        tab = []
        return len(self.skills)


class Skill(models.Model):
    user = models.IntegerField(default=1)
    technology = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(default=50)


class Framework(models.Model):
    framework = models.CharField(max_length=100, null=False)
    description = models.TextField()
    boxicons = models.TextField(default="<i class=\"bx bx-code-block\"></i>")


class Resume(models.Model):
    id = models.IntegerField(primary_key=True)
    profile = models.TextField()
    profile_1 = models.TextField()


class Education(models.Model):
    id = models.IntegerField(primary_key=True)
    degree = models.CharField(max_length=200)
    start_year = models.DateField()

    end_year = models.DateField()
    university = models.CharField(max_length=200)
    university_link = models.URLField()
    description = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class Message(models.Model):
    idUser = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


MY_CHOICES2 = ((1, 'Yes'),)


class Experience(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_year = models.DateField()
    present = MultiSelectField(choices=MY_CHOICES2, default='Yes', max_choices=1, max_length=1)

    end_year = models.DateField(null=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

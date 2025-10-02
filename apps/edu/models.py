from django.db import models

class DegreeChoices(models.TextChoices):
    BACHELORS = "BACHELORS"
    MASTERS = "MASTERS"
    PHD = "PHD"

class Major(models.Model):
    title = models.CharField(max_length=500)
    degree = models.CharField(max_length=100, choices=DegreeChoices.choices)  # e.g., B.Sc., M.Sc., Ph.D.

    def __str__(self):
        return self.title


class Field(models.Model):
    title = models.CharField(max_length=500)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="fields")

    def __str__(self):
        return self.title


class Professor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="professor-photo/", blank=True, null=True)
    university = models.ForeignKey("University", blank=True, null=True, related_name='professors')
    department = models.CharField(max_length=100, blank=True, null=True)
    research_interests = models.TextField(blank=True, null=True)
    awards_and_honors = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    fields = models.ManyToManyField(Field, related_name='professors')

    def __str__(self):
        return self.first_name + " " + self.last_name

class Education(models.Model):
    professor = models.ForeignKey("Professor", on_delete=models.CASCADE, related_name="educations")
    major = models.ForeignKey(Major, max_length=150, blank=True, null=True, on_delete=models.SET_NULL, related_name='educations')   # e.g., Computer Science
    University = models.ForeignKey('University', blank=True, null=True, on_delete=models.SET_NULL, max_length=200)  # e.g., MIT
    graduation_year = models.IntegerField(null=True, blank=True)


class Publication(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Professor)
    file = models.FileField(upload_to='publication-files/')


class Course(models.Model):
    title = models.CharField(max_length=100)
    major = models.ForeignKey(Major, blank=True, null=True, on_delete=models.SET_NULL, related_name='courses')
    professors = models.ManyToManyField(Professor, blank=True, null=True, related_name='courses')
    period = models.CharField(max_length=100)
    price = models.IntegerField()
    is_accessible = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name


class University(models.Model):
    class Meta:
        verbose_name_plural = "universities"

    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="university_logo/", blank=True, null=True)
    location = models.CharField(
        max_length=1000, blank=True, null=True
    )  # alternatively  i can  make a country choice field and put every "important" country in there
    rank = models.PositiveSmallIntegerField(blank=True, null=True)
    professors = models.ManyToManyField(
        Professor, blank=True, null=True, related_name="universities"
    )
    courses = models.ManyToManyField(Course, blank=True, null=True, related_name='universities')
    majors = models.ManyToManyField(Major, blank=True, null=True, related_name='uiversities')
    

    def __str__(self):
        return self.name

class UniversityImage(models.Model):
    image = models.ImageField(upload_to="university_image/")
    university = models.ForeignKey(University, related_name='images')
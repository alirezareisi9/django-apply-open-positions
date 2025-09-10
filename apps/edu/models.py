from django.db import models


# class Location(models.Model):
#     continent = models.TextField(blank=True)
#     country = models.TextField(blank=True)
#     state  = models.TextField(blank=True)
#     city = models.TextField(blank=True)

#     def get_content(self):
#         return f"{self.continent} + {self.country} + {self.city}" 
    
#     def __str__(self):
         
#          return self.get_content()

    
class Major(models.Model):
    title = models.CharField(max_length=500)
    def __str__(self):
        return self.title
    

class Field(models.Model):
    title = models.CharField(max_length=500)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='fields')
    def __str__(self):
        return self.title

class Professor(models.Model):  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    office_location = models.CharField(max_length=100)
    research_interests = models.TextField()
    publications = models.TextField()
    courses_taught = models.TextField()
    university = models.ManyToManyField("University", blank=True)
    biography = models.TextField()
    photo = models.ImageField(upload_to='images/')
    education = models.TextField()
    awards_and_honors = models.TextField()
    professional_associations = models.TextField()
    projects = models.TextField()
    rating = models.IntegerField()
    major = models.ManyToManyField("major")
    course = models.ManyToManyField("courses" , related_name="profcourses+")
    def __str__(self):
        return self.first_name + " " + self.last_name

                 
class Courses(models.Model):
    class Meta:
        verbose_name_plural = "Courses"
    class StudyLevelChoices(models.TextChoices):
        BACHELORS = 'BACHELORS'
        MASTERS = 'MASTERS'
        PHD = 'PHD'
    title = models.CharField(max_length=100)
    major = models.ManyToManyField(Major, blank=True)
    studylevel = models.CharField( max_length=9,choices=StudyLevelChoices.choices)
    professrs = models.ManyToManyField(Professor,blank=True)

    period = models.CharField(max_length=100)
    price = models.IntegerField()
    online = models.BooleanField(blank=True)
    on_campus = models.BooleanField(blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.name
    
    
class University(models.Model):
    class Meta:
        verbose_name_plural = "universities"
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)#alternatively  i can  make a country choice field and put every "important" country in there
    rank = models.PositiveSmallIntegerField()
    professors = models.ManyToManyField(Professor,blank=True , related_name="working_professors+")
    courses = models.ManyToManyField(Courses, blank=True)
    majors = models.ManyToManyField(Major, blank=True)
    scholarships = models.BooleanField()
    images = models.ImageField(upload_to="uni_image")
    price = models.IntegerField()
    def __str__(self):
        return self.name
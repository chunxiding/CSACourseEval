from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collegeid = models.IntegerField(default=0)
    username = models.CharField(max_length=256, default="")
    email = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=256, default="")
    website = models.URLField()
    # manytomany since crosslist; right now operate one to many
    courses = models.ManyToManyField(Course)

     def __str__(self):
         return self.username

    def get_absolute_url(self):
        return reverse('professors:department_detail', args=[str(self.id)])


class Professor(models.Model):
    # prof belongs to a department
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default="")
    email = models.TextField(blank=True, default="")
    # TODO: upload image
    image = models.ImageField(upload_to="images")
    # each prof have many courses
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('professors:professor_detail', args=[str(self.professor.id), str(self.id)])

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default="")
    description = models.TextField(blank=True,  default="")
    # each course taught by profs
    profs = models.ManyToManyField(Professor)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('professors:course_detail', args=[str(self.course.id), str(self.id)])

# This Abstract Review can be used to create ProfReview and CourseReview
class Review(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True

class ProfReview(Review):
    prof = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return "{} review".format(self.professor.name)

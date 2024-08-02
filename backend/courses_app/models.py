from django.db import models

# Create your models here.
class Course(models.Model):
    course_id = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    progress = models.CharField(max_length=10)
    

    def __str__(self) -> str:
        return f"ID: {self.course_id}, Name: {self.name}, Progress: {self.progress}"

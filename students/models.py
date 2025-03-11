from django.db import models

class Students(models.Model):
    student_id = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    branch = models.CharField(max_length=20)

    def __str__(self):
        return self.name
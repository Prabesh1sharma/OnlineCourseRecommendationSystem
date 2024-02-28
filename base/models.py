from django.db import models
from django.contrib.auth.models import User


class Watchlater(models.Model):
    save_course_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.CharField(max_length = 10000000, default = "")

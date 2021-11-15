from django.db import models


class Post(models.Model):
    post_id = models.CharField(max_length=200,primary_key=True)
    owner = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
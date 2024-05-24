from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_date",)

    def __str__(self):
        return f"Contact: {self.name} - {self.email}"


class Certificate(models.Model):
    image = models.ImageField(upload_to="certificate/%Y/%m/%d/")
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    credential_url = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"Certificate: {self.name} - {self.type}"


class Project(models.Model):
    image = models.ImageField(upload_to="project/%Y/%m/%d/")
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project: {self.name} - {self.type}"

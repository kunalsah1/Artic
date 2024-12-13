from django.db import models
from django.contrib.auth.models import User


class AssetGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(AssetGroup, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Floor(models.Model):
    name = models.CharField(max_length=255)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Units(models.Model):
    name = models.CharField(max_length=255)
    floor_id = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name= models.CharField(max_length=100)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TicketStatus(models.Model):
    name = models.CharField(max_length=255)
    color_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    floor_id = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True)
    unit_id = models.ForeignKey(Units, on_delete=models.CASCADE, null=True, blank=True)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    sub_category_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    complaint_type = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_assigned', null=True,blank=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    venue = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(null=True, blank=True)
    send_email = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    individual_users = models.ManyToManyField(User, related_name='invited_users', blank=True)
    event_image = models.FileField(upload_to='attachments/', blank=True, null=True)


    def __str__(self):
        return self.event_name







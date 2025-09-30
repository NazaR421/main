from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    likes_count = models.IntegerField()
    user_email = models.EmailField()
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["created_at"]
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=99)
    description = models.TextField(blank=True)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.room.name} {self.start_date} {self.end_date}"
    

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Не правильна дата")
        overlapping_bookings = Booking.objects.filter(
            room = self.room,
            start_date__lte = self.end_date,
            end_date__gte = self.start_date
        ). exclude(id=self.id)
        if overlapping_bookings.exists():
            raise ValidationError("Ця кімната заброньована")
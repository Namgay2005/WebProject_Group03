from django.db import models

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    total_rooms = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='hostels/')

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    number = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.number}"

from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city =models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"



class flight(models.Model):
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE, related_name='departure')
    destination =models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival')
    duration=models.IntegerField()

    def is_valid_flight(self):
        return (self.origin != self.destination) and (self.duration >= 0)

    def __str__(self):
        return f'{self.id} - {self.origin} to {self.destination} - {self.duration} minutes'





class passenger(models.Model):
    first=models.CharField(max_length=64)
    last=models.CharField(max_length=64)
    flights =models.ManyToManyField(flight,blank=True,related_name='passenger' )

    def __str__(self):
        return f'{self.first} {self.last}'

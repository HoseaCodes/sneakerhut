from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

PURCHASES = (
    ('N', 'New Release'),
    ('R', 'Resale'),
    ('D', 'Deadstock'),
)
# Create your models here.
class Shoelace(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('shoelace_detail', kwargs={'pk': self.id })

class Sneaker(models.Model):
    name = models.CharField(max_length=50)
    style = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    shoelaces = models.ManyToManyField(Shoelace)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def purchase_for_today(self):
        return self.purchase_set.filter(date=date.today()).count() >= len(PURCHASES)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'sneaker_id': self.id})

class Purchase(models.Model):
    date = models.DateField('purchase date')
    purchase = models.CharField(
      max_length=1,
      choices=PURCHASES,
      default=PURCHASES[0][0])
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)


    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_purchase_display()} on {self.date}"
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for sneaker_id: {self.sneaker_id} @{self.url}"
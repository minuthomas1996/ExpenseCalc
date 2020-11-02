from django.db import models

class Cat_gst(models.Model):
    category=models.CharField(max_length=200)
    gst=models.FloatField()

    def __str__(self):
        return self.category

class Expense(models.Model):
    date = models.DateField()
    description = models.CharField(max_length = 200)
    category = models.ForeignKey(Cat_gst,on_delete=models.CASCADE)
    amount = models.FloatField()
    username = models.CharField(max_length=200)
    gsttot=models.FloatField(null=True)

    class Meta:
        verbose_name="ex table"

    def __str__(self):
        return self.category.category

from django.db          import models
from models        import TimeStampModel

class User(TimeStampModel):
    name         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    email        = models.CharField(max_length=200,unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

# customized User model
class User(AbstractUser):
    id = models.CharField(max_length=8, primary_key=True, editable=False)


    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        username = self.username
        current_time = timezone.now().strftime('%Y%m%d%H%M%S')
        sample = f"{username[:4]}{current_time[-4:]}"
        rand_sample = random.sample(sample, k=8)
        unique_id = ''.join(rand_sample)
        self.id = unique_id

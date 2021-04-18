from django.db import models
import hashlib, random, string
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
def randomStr(minLen, maxLen):
    strLen = random.choice(range(minLen,maxLen))
    return ''.join(random.choice(string.ascii_lowercase) for i in range(strLen))

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(unique=True,max_length=50)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    #  RANDOM ID FROM 20 TO 50 VARIABLE LENGTH
    def generate_id(self):
        minLen = 15
        maxLen = 46
        valid_lengths = range(minLen, maxLen)
        idLen = random.choice(valid_lengths)
        seed = hashlib.md5(self.title.encode('utf-8')).hexdigest()
        seed += hashlib.md5(self.description.encode('utf-8')).hexdigest()
        seed += hashlib.md5(randomStr(minLen,maxLen).encode('utf-8')).hexdigest()
        last_part = hashlib.sha224(seed.encode('utf-8')).hexdigest()[:idLen]
        today = date.today()
        first_part = hashlib.md5(self.title.encode('utf-8')+str(today.year+today.month).encode('utf-8')).hexdigest()
        new_id = first_part[:5] + last_part
        self.uuid = new_id.upper()

    def save(self, *args, **kwargs):
        if not self.uuid:
           self.generate_id()
        super(Collection, self).save(*args, **kwargs)

class Movie(models.Model):
    uuid = models.CharField(unique=True,max_length=50)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    genres = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    #  RANDOM ID FROM 20 TO 50 VARIABLE LENGTH
    def generate_id(self):
        minLen = 15
        maxLen = 46
        valid_lengths = range(minLen, maxLen)
        idLen = random.choice(valid_lengths)
        seed = hashlib.md5(self.title.encode('utf-8')).hexdigest()
        seed += hashlib.md5(self.description.encode('utf-8')).hexdigest()
        seed += hashlib.md5(randomStr(minLen,maxLen).encode('utf-8')).hexdigest()
        last_part = hashlib.sha224(seed.encode('utf-8')).hexdigest()[:idLen]
        today = date.today()
        first_part = hashlib.md5(self.title.encode('utf-8')+str(today.year+today.month).encode('utf-8')).hexdigest()
        new_id = first_part[:5] + last_part
        self.uuid = new_id.upper()

    def save(self, *args, **kwargs):
        if not self.uuid:
           self.generate_id()
        super(Movie, self).save(*args, **kwargs)

class RequestCounter(models.Model):
    count = models.IntegerField(default=0)
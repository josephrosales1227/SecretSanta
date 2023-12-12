from django.db import models
from django.contrib.auth.models import User
import string
import random

def generateGroupCode():
    length = 10
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if not Group.objects.filter(code=code).exists():
            break
    return code

# Create your models here.
class Group(models.Model):
    code = models.CharField(max_length=10, default=generateGroupCode, unique=True, primary_key=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    numberOfParticipants = models.IntegerField()
    budget = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Relation(models.Model):
    # Group Code should be related to the Group model and its code
    groupCode = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False)

    # Giver will be the name of the person who is going to be giving the gift
    giver = models.CharField(max_length=200, blank=False)

    # Receiver will be the name of the person who is getting the gift from the giver
    receiver = models.CharField(max_length=200, blank=False)

    # Individual Code will be a generated code at the time the Group is created. For each person, a code will be generated for them to use to 
    # retrieve who they(giver) will be giving a gift to(receiver)
    individualCode = models.CharField(max_length=10, blank=False)
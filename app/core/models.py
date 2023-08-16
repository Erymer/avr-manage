import uuid
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

ROLE_CHOICES = (
    ('sales', 'Ventas'),
    ('tech', 'Técnico'),
    ('admin', 'Administrativo'),
    ('finance', 'Finanzas'),
    ('inventory', 'Inventario'),
)


def event_photo_path(instance, filename):
    '''
    Generate file path for new event photo.
    '''
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'events', 'photos', filename)


def event_file_path(instance, filename):
    '''
    Generate file path for new event file.
    '''
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'events', 'files', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, email, password=None, **extra_fields):
        '''
        Create, save and return a new user
        '''
        if not email:
            raise ValueError('Employee must have an email address')

        if not username:
            raise ValueError('Employee must have a username')

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_superuser(self, username, email, password, **extra_fields):
        '''
        Create and return a new superuser
        '''
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Employee(AbstractBaseUser, PermissionsMixin):
    """Model representing an employee of the company"""
    ROLE_CHOICES = (
        ('sales', 'Ventas'),
        ('tech', 'Técnico'),
        ('admin', 'Administrativo'),
        ('finance', 'Finanzas'),
    )
    username = models.CharField(max_length=20, unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    fathers_name = models.CharField(max_length=20, null=False)
    mothers_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'


class Venue(models.Model):
    """Venue where an event will take place"""
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.name


class Client(models.Model):
    """Client of the company"""
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class EquipmentModel(models.Model):
    """Model of equipment"""
    name = models.CharField(unique=True, max_length=50, null=False)

    def __str__(self):
        return self.name


class EquipmentBrand(models.Model):
    """Brand of the equipment"""
    name = models.CharField(unique=True, max_length=50, null=False)

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    """Type of equipment (microphone, speaker etc.)"""
    name = models.CharField(unique=True, max_length=50, null=False)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Device"""
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE) 
    brand = models.ForeignKey(EquipmentBrand, on_delete=models.CASCADE)
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    number = models.IntegerField(null=False)
    uid = models.CharField(unique=True)
    serial_number = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        model_id = str(self.model.id).zfill(2)
        brand_id = str(self.brand.id).zfill(2)
        type_id = str(self.type.id).zfill(2)
        number = str(self.number)
        self.uid = f"{model_id}{brand_id}{type_id}-{number}"
        super(Equipment, self).save(*args, **kwargs)

    def __str__(self):
        return self.uid


class Event(models.Model):
    """Event or equipment loan."""

    name = models.CharField(max_length=50)
    load_in_date = models.DateTimeField()
    load_out_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    equipment = models.ManyToManyField(Equipment)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    crew = models.ManyToManyField(Employee, related_name="event_crew")
    leader = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name="event_leader", null=True)
    comment = models.TextField()

    def __str__(self):
        return self.name


class EventPhoto(models.Model):
    """Photo of an event"""
    photo = models.ImageField(upload_to=event_photo_path)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)


class EventFile(models.Model):
    """File used for an event"""
    file = models.FileField(upload_to=event_file_path)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)

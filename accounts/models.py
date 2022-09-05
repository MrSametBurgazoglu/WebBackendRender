from django.db import models
from django.contrib.auth.models import User
from cars.models import Car, Location


class Campaign(models.Model):
    campaign_start_day = models.DateTimeField()
    campaign_end_day = models.DateTimeField()
    campaign_code = models.CharField(max_length=16)
    campaign_info = models.CharField(max_length=128)


class Penalty(models.Model):
    penalty_price = models.IntegerField(default=0)
    penalty_info = models.CharField(max_length=128)


class PaymentMethod(models.Model):
    information = models.CharField(verbose_name="Kart Bilgileri", max_length=64)
    name = models.CharField(verbose_name="İsim", max_length=64)
    owner_name = models.CharField(verbose_name="Sahibin İsim", max_length=64)
    number = models.IntegerField(verbose_name="Kart No", default=0)
    csv = models.IntegerField(verbose_name="Kart No", default=0)
    last_month = models.IntegerField(verbose_name="geçerli son ay", default=0)
    last_year = models.IntegerField(verbose_name="geçerli son yıl", default=0)


class Address(models.Model):
    title = models.CharField(max_length=64)
    street_no = models.CharField(max_length=32)
    floor = models.CharField(max_length=64)
    flat = models.CharField(max_length=64)
    directions = models.CharField(max_length=64)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class PlateLicence(models.Model):
    full_name = models.CharField(verbose_name="İsim Soyisim", max_length=128)
    place = models.CharField(verbose_name="Verilme yeri", max_length=128)
    document_no = models.IntegerField(verbose_name="Belge No", default=0)
    date = models.DateTimeField(verbose_name="İlk belge tarihi")
    candidate = models.BooleanField(verbose_name="Aday Sürücü", default=False)
    serial_no = models.CharField(verbose_name="Seri Numarası", max_length=64)
    licence_type = models.CharField(verbose_name="Ehliyet Sınıfı", max_length=16)


class BlackListMember(models.Model):
    plate_licence = models.OneToOneField(PlateLicence, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=128)


class Customer(models.Model):
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plate_licence = models.OneToOneField(PlateLicence, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(verbose_name="İsim Soyisim", max_length=64)
    photo = models.ImageField(verbose_name="A photo of car", upload_to=None, height_field=None, width_field=None,
                              max_length=100, null=True, blank=True)
    full_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True)
    cars = models.ManyToManyField(Car, through='Journey')  # TODO RECONSIDER THIS OPTION
    phone_number = models.CharField(max_length=15)  # django phonenumber field
    email = models.EmailField(max_length=128)
    approved = models.BooleanField(default=False)
    active_user = models.BooleanField(default=False)
    #penalty = models.ForeignKey(Penalty, on_delete=models.CASCADE, null=True)
    #campaign_code = models.ManyToManyField(Campaign) # campaign class

    def __str__(self):
        return str(self.user)


class Journey(models.Model):
    cost = models.FloatField(default=0.0)
    total_minute = models.IntegerField(default=0)
    total_distance = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    start_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="start_location")
    end_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="end_location")
    user = models.ForeignKey(Customer, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)

# Create your models here.

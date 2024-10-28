from django.db import models
from utils.models import BaseModel
from utils.choices import (
    OrganizationsType, OrganizationsRatingType,
    MeasureType, EquipmentType, AvilableType,

)
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.contrib.auth.models import User

#! Viloay uchun model 


class Regions(BaseModel):
    name = models.CharField(max_length=32, unique=True, validators=[MinLengthValidator(limit_value=6, message="Viloyat nomi juda qisqa, noto'g'ri kiritgansiz")])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ['name']
    
#! /Viloyat uchun model


#! Tuman uchun model

class Districts(BaseModel):
    region = models.ForeignKey('school.Regions', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, validators=[MinLengthValidator(limit_value=5, message="Tuman nomi juda qisqa, noto'g'ri kiritgansiz")])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"

#! /Tuman uchun model


#! Shaxar uchun model

class Cities(BaseModel):
    region = models.ForeignKey('school.Regions', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, validators=[MinLengthValidator(limit_value=5, message="Shaxar nomi juda qisqa, noto'g'ri kiritgansiz")])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Shaxar"
        verbose_name_plural = "Shaxarlar"

#! Shaxar uchun model


#! Muassasa

class Organizations(BaseModel):
    organization_number = models.PositiveIntegerField()
    name = models.CharField(max_length=64, validators=[MinLengthValidator(limit_value=5, message="Muassasa nomi juda qisqa, noto'g'ri kiritgansiz")])
    education_type = models.CharField(max_length=32, choices=OrganizationsType.choices)
    power = models.PositiveBigIntegerField(default=0)
    vr_mode_url = models.URLField(null=True, blank=True)
    is_inclusive = models.BooleanField(default=False)
    rating = models.CharField(max_length=16, choices=OrganizationsRatingType.choices, null=True, blank=True)

    district = models.ForeignKey(Districts, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, null=True, blank=True)

    is_city = models.BooleanField(default=False) # Shahar yoki tumanligini ajratish uchun
    
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)

    ball = models.PositiveBigIntegerField(default=0)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Muassasa"
        verbose_name_plural = "Muassasa"
        ordering = ['-ball']

#! / Muassasa 


#! Umumiy sinflar

class OverallClasses(BaseModel):
    organization = models.ForeignKey('school.Organizations', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    rooms_amount = models.PositiveSmallIntegerField(default=1, help_text="Xonalar soni")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Umumiy sinf"
        verbose_name_plural = "Umumiy sinflar"
#! /Umumiy sinflar 


#! Rooms category

class RoomsType(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Xona turi"
        verbose_name_plural = "Xonalar turlari"

#! /Rooms category 


#! Xona jihozlari

class RoomsEquipment(BaseModel):
    name = models.CharField(max_length=256, validators=[MinLengthValidator(3, "Jihoz nomi juda qisqa, xato kiritgan bo'lishingiz mumkin !")])
    measure_type = models.CharField(max_length=8, choices=MeasureType.choices)
    amount = models.PositiveBigIntegerField(default=1) # shu jihozdan nechtaligi

    avilable_type = models.CharField(max_length=32, choices=AvilableType.choices)

    accepted_date = models.DateField() # bu jihoz(lar) qachon olib kelingan

    entered_date = models.DateField() # bu jihoz qachon kirim qilindi

    when_first_time_used = models.DateField() #qachon_foydalanildi

    when_made = models.PositiveIntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2024)], null=True, blank=True) #shu_jihoz_qachon_ishlab_chiqarilganligi


    
    image1 = models.ImageField(upload_to='school/rooms/equipement/', null=True, blank=True)
    image2 = models.ImageField(upload_to='school/rooms/equipement/', null=True, blank=True)
    image3 = models.ImageField(upload_to='school/rooms/equipement/', null=True, blank=True)

    penny_by_year = models.FloatField() # yiliga qancha foiz eskirish foizi

    xarakteri = models.TextField(null=True, blank=True)

    equipment_type = models.CharField(max_length=16, choices=EquipmentType.choices)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Xona jihozi"
        verbose_name_plural = "Xonalar jihozlari"
    
#! /Xona jihozlari

#! Xonalar

class Rooms(BaseModel):
    room_category = models.ForeignKey(RoomsType, on_delete=models.SET_NULL, null=True, blank=True) # misol uchun informatika xonasi
    students_amount = models.PositiveSmallIntegerField(default=1) # sinf xonadagi o'quvchilar sig'imi
    room_uquipment = models.ManyToManyField(RoomsEquipment)

    def __str__(self):
        return self.room_category.name
    
    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"

#! /Xonalar


#! SchoolStatistics

class OrganizationStatistics(BaseModel):
    type = models.CharField(max_length=32, choices=OrganizationsType.choices, unique=True)
    number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Tashkilot turi"
        verbose_name_plural = "Tashkilot turlari"

#! /SchoolStatistics

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_profile')
    first_name = models.CharField(max_length=32, default="No Name")
    last_name = models.CharField(max_length=32, default="No Last Name")
    born_in = models.DateField()
    father_name = models.CharField(max_length=32)
    passport_id = models.CharField(max_length=9, unique=True)
    manzil = models.CharField(max_length=512)
    pinfl = models.CharField(max_length=14, unique=True)
    position = models.CharField(max_length=512)
    tel_number = models.CharField(max_length=9)

    command_expire = models.DateField(null=True, blank=True) # buyruq tugash vaqti
    command_pdf = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]) # pdf file Buyrug' (Moddiy texnik baza bo'yicha mas'ul shaxs buyrug'i)

    is_active = models.BooleanField(default=True)
    is_selected = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def fio(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def get_uuid(self):
        return self.id

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchilar profillari"


# class SetOrganizationAdmin(BaseModel):
#     admin = models.ForeignKey(UserProfile, related_name='admin_profile', on_delete=models.CASCADE)
#     organization = models.ForeignKey(Organizations, related_name='admin_organization', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = "Admin tayinlash"
#         verbose_name_plural = "Admin tayinlash"
#         unique_together = ['admin', 'organization']
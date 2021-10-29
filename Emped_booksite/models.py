from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from datetime import date
import re
from phonenumber_field.modelfields import PhoneNumberField


# Category model
class Category(models.Model):
    Name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    Image = models.ImageField(upload_to="Genres_images", null=True)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('Genres-detail', args=[str(self.id)])

    @property
    def preview(self):
        return format_html(f'<img src="/media/{self.Image}" style="height:100px; width:100px">')


# Age Range model
class Range(models.Model):
    AgeRange = models.CharField(max_length=20, help_text='Enter the age_range')  # validation yet to be done
    Image = models.ImageField(upload_to="Range_images")
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.AgeRange

    def get_absolute_url(self):
        return reverse('Range-detail', args=[str(self.id)])

    @property
    def preview(self):
        return format_html(f'<img src="/media/{self.Image}" style="height:100px; width:100px">')


# Author model
class Author(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to="Author_images", null=True)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('Author-detail', args=[str(self.id)])

    @property
    def preview(self):
        return format_html(f'<img src="/media/{self.Image}" style="height:100px; width:100px">')


# Products model
class Book(models.Model):
    Name = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="Product_images")
    Description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    Genre = models.ManyToManyField(Category, help_text='Select a genre for this book')
    Age = models.ForeignKey(Range, on_delete=models.CASCADE, default=Range.objects.only('id').get(AgeRange='Adult').id)
    Author = models.ManyToManyField(Author, help_text='Select a author of this book')
    Price1 = models.FloatField(default=0)
    Price2 = models.FloatField(default=0)
    Price3 = models.FloatField(default=0)
    Price4 = models.FloatField(default=0)
    Publisher = models.CharField(max_length=50, blank=True)
    Product_status = (('Available', 'Available'), ('Rented', 'Rented'), ('Damaged', 'Damaged'))
    Status = models.CharField(choices=Product_status, max_length=9, default='Available')
    CreatedAt = models.DateField(auto_now_add=True, null=True)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    @property
    def preview(self):
        return format_html(f'<img src="/media/{self.Image}" style="height:100px; width:100px">')


# Customer model

class Customer(models.Model):
    PhoneNo = PhoneNumberField(null=False, blank=False, unique=True)
    OTP = models.IntegerField(blank=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.PhoneNo.as_e164

    def get_absolute_url(self):
        return reverse('personal_info', args=[str(self.id)])


# Customer Address
class CustomerAddress(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    DoorNo = models.CharField(max_length=20)
    Address = models.TextField()
    PinCode = models.CharField(max_length=6)
    LandMark = models.CharField(max_length=100)
    IsDefault = models.BooleanField(default=False)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('customerAddress', args=[str(self.id)])


# Rent Model
class Rent(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    CustomerAddress = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    StartDate = models.DateField(auto_now_add=True, null=True)
    Order_status = (('Returned', 'Returned'), ('On Rent', 'On Rent'))
    Status = models.CharField(choices=Order_status, max_length=8, default='On Rent')
    ReturnedDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def rent_price(self):
        if self.Status == 'On Rent':
            difference = date.today() - self.StartDate
        else:
            difference = self.ReturnedDate - self.StartDate
        if difference.days > 28:
            return self.Book.Price4
        elif difference.days > 21:
            return self.Book.Price3
        elif difference.days > 14:
            return self.Book.Price2
        else:
            return self.Book.Price1

    def get_absolute_url(self):
        return reverse('notify', args=[str(self.id)])


# Cart Model
class Cart(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)
    IsSaveForLater = models.BooleanField(default=False)
    IsWishList = models.BooleanField(default=False)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)




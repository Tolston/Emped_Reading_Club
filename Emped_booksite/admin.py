from django.contrib import admin
from .models import *
from django.utils.html import format_html


# Register your models here.

admin.site.site_header = 'Emped Reading Club And Learning Pvt Ltd '


# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Edit', 'Name', 'IsDeleted')
    list_display_links = None
    readonly_fields = ('preview',)

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/category/{obj.id}/change/" class="button default">edit</a>')


admin.site.register(Category, CategoryAdmin)


# Age Range Admin
class RangeAdmin(admin.ModelAdmin):
    fields = ('AgeRange', 'Image', 'IsDeleted')
    list_display = ('Edit', 'id', 'AgeRange', 'Image', 'IsDeleted')
    list_display_links = None
    readonly_fields = ('preview',)

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/range/{obj.id}/change/" class="button default">edit</a>')


admin.site.register(Range, RangeAdmin)


# Author Admin
class AuthorAdmin(admin.ModelAdmin):
    fields = ('Name', 'Image', 'IsDeleted')
    list_display = ('Edit', 'Name', 'Image', 'IsDeleted')
    list_display_links = None
    readonly_fields = ('preview',)

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/author/{obj.id}/change/" class="button default">edit</a>')


admin.site.register(Author, AuthorAdmin)


# Product Admin
class BookAdmin(admin.ModelAdmin):
    fields = ('Name', ('Image', 'preview'), 'Description', 'Genre', 'Age', 'Author',
              ('Price1', 'Price2', 'Price3', 'Price4'), 'Publisher', 'Status')
    list_display = ('Edit', 'Name', 'picture', 'description', 'Authors', 'Genres', 'Age',
                    'Price1', 'Price2', 'Price3', 'Price4', 'Publisher', 'Status')
    list_display_links = None
    readonly_fields = ('preview',)

    def picture(self, obj):
        if len(obj.Image.url) > 41:
            return format_html(f'<a href="/media/{obj.Image}">{obj.Image.url[21:41]}..</a>')
        else:
            return format_html(f'<a href="/media/{obj.Image}">{obj.Image.url[21:]}</a>')

    def description(self, obj):
        return obj.Description[:20]

    def Genres(self, obj):
        return ", ".join([b.Name for b in obj.Genre.all()])

    def Authors(self, obj):
        return ", ".join([b.Name for b in obj.Author.all()])

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/book/{obj.id}/change/" class="button default">edit</a>')


admin.site.register(Book, BookAdmin)


# Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    fields = ('PhoneNo', 'OTP', ('FirstName', 'LastName'), 'IsDeleted')
    list_display = ('Edit', 'PhoneNo', 'OTP', 'FirstName', 'LastName')
    list_display_links = None

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/customer/{obj.id}/change/" class="button default">edit</a>')


admin.site.register(Customer, CustomerAdmin)


# CustomerAddress Admin
class CustomerAddressAdmin(admin.ModelAdmin):
    fields = ('Customer', 'DoorNo', 'Address', 'PinCode', 'LandMark', 'IsDefault', 'IsDeleted')
    list_display = ('Edit', 'Customer', 'DoorNo', 'Address', 'PinCode', 'LandMark', 'IsDefault', 'IsDeleted')
    list_display_links = None

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/customeraddress/{obj.id}/change/" '
                           f'class="button default">edit</a>')


admin.site.register(CustomerAddress, CustomerAddressAdmin)


# Rent Admin
class RentAdmin(admin.ModelAdmin):
    fields = ('Book', 'Customer', 'CustomerAddress', 'Status', 'ReturnedDate')
    list_display = ('Edit', 'Book', 'Customer', 'CustomerAddress', 'StartDate', 'Status', 'ReturnedDate', 'rent_price',
                    'notify')
    list_display_links = None
    readonly_fields = ('StartDate', 'rent_price',)

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/rent/{obj.id}/change/" class="button default">edit</a>')

    def notify(self, obj):
        return format_html(f'<a href="{obj.get_absolute_url}" class="button default">notify</a>')


admin.site.register(Rent, RentAdmin)


# Cart Admin
class CartAdmin(admin.ModelAdmin):
    fields = ('Book', 'Customer', 'IsActive', 'IsSaveForLater', 'IsDeleted')
    list_display = ('Edit', 'Book', 'Customer', 'IsActive', 'IsSaveForLater', 'IsWishList', 'IsDeleted')
    list_display_links = None

    def Edit(self, obj):
        return format_html(f'<a href="/admin/Emped_booksite/cart/{obj.id}/change/" class="button default">edit</a>')


admin.site.register(Cart, CartAdmin)

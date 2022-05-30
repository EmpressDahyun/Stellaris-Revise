from secrets import choice
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

BARANGAY_CHOICES = (
    ('Ayala', 'Ayala'),
    ('Baliwasan', 'Baliwasan'),
    ('Boalan', 'Boalan'),
    ('Cabatangan', 'Cabatangan'),
    ('Calarian', 'Calarian'),
    ('Campo Islam', 'Campo Islam'),
    ('Canelar', 'Canelar'),
    ('Cawit', 'Cawit'),
    ('City Proper', 'City Proper'),
    ('Divisoria', 'Divisoria'),
    ('Guiwan', 'Guiwan'), 
    ('Lumbangan', 'Lumbangan'),
    ('Lunzuran', 'Lunzuran'),
    ('Maasin', 'Maasin'),
    ('Malagutay', 'Malagutay'),
    ('Pasonanca', 'Pasonanca'), 
    ('Putik	', 'Putik'),
    ('Recodo', 'Recodo'),
    ('San Jose Cawa-cawa', 'San Jose Cawa-cawa'),
    ('San Jose Gusu', 'San Jose Gusu'),
    ('San Roque', 'San Roque'),
    ('Santa Maria', 'Santa Maria'),
    ('Santo Niño', 'Santo Niño'),
    ('Sinunoc', 'Sinunoc'),
    ('Talon-talon', 'Talon-talon'),
    ('Tetuan', 'Tetuan'),
    ('Tumaga', 'Tumaga'),
    ('Zambowood', 'Zambowood'),
)

class DeliveryInformation(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, verbose_name="Recipient's Fullname", blank=False) 
    phone_number = models.CharField(max_length=13, default="+63", verbose_name="Phone Number", blank=False)
    barangay = models.CharField(max_length=150, choices=BARANGAY_CHOICES, default="Ayala" ,verbose_name="Barangay", blank=False)
    landmark = models.CharField(max_length=150, verbose_name="Landmark", blank=False)
    location = models.CharField(max_length=150, verbose_name="Location", blank=False)
    notes = models.TextField(verbose_name="Customer Notes")
    def __str__(self):
        return self.barangay

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price

class Favorites(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Customer Favorites'

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)
    
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    address = models.ForeignKey(DeliveryInformation, verbose_name="Address", on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(verbose_name="Total Price")
    remarks = models.TextField(verbose_name="Remarks", blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
    )   

class OrderItem(models.Model):
    invoice_no=models.CharField(max_length=150)
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.DecimalField(max_digits=8, decimal_places=2) 

    @property
    def total_price(self):
        return self.quantity * self.product.price

class OrderManagement(models.Model):
    invoice_no=models.CharField(max_length=150)
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.DecimalField(max_digits=8, decimal_places=2) 

    @property
    def total_price(self):
        return self.quantity * self.product.price

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Cancelled', 'Cancelled')
)

GUESS_LIMIT = (
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('25', '25'),
    ('30', '30'),
    ('35', '35'),
    ('40', '40'),
    ('45', '45'),
    ('50', '50'),
)

class Reservation(models.Model):
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, default="+63", verbose_name="Phone Number", blank=False)
    pax = models.CharField(max_length=13,verbose_name="Number of Guest", choices=GUESS_LIMIT ,default=30, null=False)
    pax_expected = models.CharField(max_length=13,verbose_name="Number of Walk-in Guest", choices=GUESS_LIMIT ,default=30, null=False)
    event_name = models.CharField(verbose_name="Event Name", max_length=150, null=False) 
    event_type = models.CharField(verbose_name="Event Type", max_length=150, null=False)
    event_date = models.DateField(verbose_name="Event Date", unique=True)
    event_time = models.TimeField(verbose_name="Event Time", unique=True)
    event_time_end = models.TimeField(verbose_name="Event Time End")
    remarks = models.TextField(verbose_name="Remarks", blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )

    def __str__(self):
        return self.event_name

class Gallery(models.Model):
    description = models.CharField(verbose_name="Description", max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery", blank=True, null=True, verbose_name="Gallery Image")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name_plural = "Gallery"

class ProductReservation(models.Model):
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, verbose_name="Recipient Name", blank=False)
    phone_number = models.CharField(max_length=13, default="+63", verbose_name="Phone Number", blank=False)
    delivery_time = models.TimeField(verbose_name="Delivery Time")
    pickup_date = models.DateField(verbose_name="Pickup Date")
    remarks = models.TextField(verbose_name="Remarks", blank=True)

    def __str__(self):
        return self.fname 

class Sales(models.Model):
    total_orders = models.PositiveIntegerField("Total Orders")
    total_products = models.PositiveIntegerField("Total Products Listed")
    revenue = models.PositiveIntegerField("Total Revenue")
    subtotal = models.PositiveIntegerField("Total Wholesale Price")
    report_date = models.DateTimeField(verbose_name="Report Date", auto_now_add=True)

    def __str__(self):
        return str(self.total_orders)




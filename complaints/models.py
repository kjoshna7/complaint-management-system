from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):

    # Status Choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    # Priority Choices
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    # Complaint Categories
    CATEGORY_CHOICES = [
        ('Water', 'Water'),
        ('Road', 'Road'),
        ('Electricity', 'Electricity'),
        ('Garbage', 'Garbage'),
        ('Street Light', 'Street Light'),
        ('Other', 'Other'),
    ]

    # Basic Complaint Information
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()

    # Location Details
    state = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    address = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=10)

    # Map Coordinates (Used for Map Feature)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Complaint Priority
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Low',
        db_index=True
    )

    # Image Upload
    image = models.ImageField(
        upload_to='complaints/',
        null=True,
        blank=True
    )

    # Complaint Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        db_index=True
    )

    # Resolution details
    resolution_remarks = models.TextField(blank=True, default='')

    # User who submitted complaint
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    # Timestamp Fields
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Full Address Helper
    def full_address(self):
        parts = [self.address, self.city, self.state, self.zipcode]
        return ", ".join(filter(None, parts))

    # Display Name in Admin
    def __str__(self):
        return f"{self.title} - {self.city} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Complaint"
        verbose_name_plural = "User Complaints"


class Notification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
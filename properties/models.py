from django.db import models
from decimal import Decimal


class Property(models.Model):
    """
    Property model for real estate listings
    """
    title = models.CharField(max_length=200, help_text="Property title/name")
    description = models.TextField(help_text="Detailed property description")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Property price in currency"
    )
    location = models.CharField(max_length=100, help_text="Property location/address")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - ${self.price} ({self.location})"

    def formatted_price(self):
        """Return formatted price string"""
        return f"${self.price:,.2f}"

    @property
    def is_expensive(self):
        """Check if property is expensive (over $500,000)"""
        return self.price > Decimal('500000.00')
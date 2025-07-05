from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Added
    duration = models.CharField(max_length=100, default="1 month")  # Added
    status = models.CharField(max_length=50, default='active')  # 'active', 'upcoming', 'completed'
    created_at = models.DateTimeField(auto_now_add=True)  # Added
    updated_at = models.DateTimeField(auto_now=True)  # Added

    def __str__(self):
        return self.name

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='scheduled')  # 'scheduled', 'completed', 'cancelled'
    created_at = models.DateTimeField(auto_now_add=True)  # Added
    updated_at = models.DateTimeField(auto_now=True)  # Added

    def __str__(self):
        return f"{self.course.name} - {self.start_time}"

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    enrolled_services = models.ManyToManyField(Course, through='Enrollment')
    status = models.CharField(max_length=50, default='active')  # 'active', 'inactive'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='enrolled')  # 'enrolled', 'completed', 'dropped'
    created_at = models.DateTimeField(auto_now_add=True)  # Added
    updated_at = models.DateTimeField(auto_now=True)  # Added

    def __str__(self):
        return f"{self.client.name} - {self.course.name}"

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Keep as 'course'
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')  # 'paid', 'pending', 'cancelled'
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Changed from total_amount
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.client.name}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')  # 'completed', 'failed', 'pending'
    created_at = models.DateTimeField(auto_now_add=True)  # Added
    updated_at = models.DateTimeField(auto_now=True)  # Added

    def __str__(self):
        return f"Payment {self.id} - {self.order.client.name}"

class Enquiry(models.Model):
    name = models.CharField(max_length=255)  # Added
    email = models.EmailField()  # Added
    phone = models.CharField(max_length=20)  # Added
    service = models.CharField(max_length=255)  # Added - what service they're interested in
    message = models.TextField()
    status = models.CharField(max_length=50, default='new')  # Added - 'new', 'contacted', 'closed'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry from {self.name} at {self.created_at}"

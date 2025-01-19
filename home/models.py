from django.db import models
from django.contrib.auth.models import User

class ShowQR(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="qrs/", blank=True, null=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=255, default="Unnamed Post")
    image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    content = models.TextField(blank=True, default="No content provided.")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} - {self.title}'
    

class Event(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Event")
    description = models.TextField(blank=True, default="No description provided.")
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, related_name='event_participants', blank=True)
    is_frozen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.organizer.username} - {self.name}'

    def is_user_participating(self, user):
        return self.participants.filter(pk=user.pk).exists()

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_image = models.ImageField(upload_to='payments/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='Pending')
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="donations_approved")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blog_post.title} - {self.user.username} - ₹{self.amount}"
    
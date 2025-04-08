from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Question(models.Model):
    user = models.ForeignKey(User, related_name="questions", on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(User, related_name="questions_followed", blank=True)

    def number_of_followers(self):
        return self.followers.count()

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%d-%m-%Y %H:%M}):"
            f"{self.body}..."
            )
    
class Answer(models.Model):
    user = models.ForeignKey(User, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="answers_liked", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%d-%m-%Y %H:%M}):"
            f"{self.body}..."
            )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

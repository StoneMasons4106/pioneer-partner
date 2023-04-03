from django.db import models
from django.contrib.auth.models import User
from congregations.models import Congregation
import random
import string

# Create your models here.

class Post(models.Model):

    post_id = models.CharField(max_length=32, null=False, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, null=True, blank=True)
    text_input = models.TextField(max_length=512)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    bookmarks = models.ManyToManyField(User, blank=True, related_name='post_bookmarks')
    created = models.DateTimeField(auto_now_add=True)

    def _generate_post_id(self):
        """
        Generate a random, unique post ID using UUID
        """
        output_string = ''.join(random.SystemRandom().choice(string.ascii_letters.lower() + string.digits) for _ in range(32))
        return output_string

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.post_id:
            self.post_id = self._generate_post_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.post_id

    def number_of_likes(self):
        return self.likes.count()

    def number_of_bookmarks(self):
        return self.bookmarks.count()

    def number_of_comments(self):
        comments = len(Comment.objects.filter(original_post=self.id))
        return comments

    def is_liked(self):
        return self.likes.all()

    def is_bookmarked(self):
        return self.bookmarks.all()


class Comment(Post):

    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
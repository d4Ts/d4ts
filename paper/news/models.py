from django.db import models

from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    connect = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('ratingPost'))
        pRat = 0
        pRat += postRat.get('postRating')
        comrat = self.connect.comment_set.aggregate(CommentRating=Sum('ratingCom'))
        cRat = 0
        cRat += comrat.get('CommentRating')
        self.rating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name_of_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    a_or_n = [
        ('article', 'Статья'),
        ('news', 'Новость')
    ]
    connection = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_or_article = models.CharField(max_length=255, choices=a_or_n)
    datetime_of_appear = models.DateTimeField(auto_now_add=True)
    many_to_many = models.ManyToManyField(Category, through='PostCategory')
    heading_of_article = models.CharField(max_length=255)
    text_of_article = models.TextField()
    ratingPost = models.IntegerField(default=0)

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    def preview(self):
        return f'{self.text_of_article[:124]}...'

    def __str__(self):
        return f'{self.heading_of_article}:{self.text_of_article[:20]}'




class PostCategory(models.Model):
    connectionPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    connectionCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    connectionPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    connectionUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text_of_comment = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    ratingCom = models.IntegerField(default=0)

    def like(self):
        self.ratingCom += 1
        self.save()

    def dislike(self):
        self.ratingCom -= 1
        self.save()



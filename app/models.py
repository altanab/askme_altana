from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


class LikeDislikeManager(models.Manager):
    def liked(self):
        return self.filter(like=True)

    def disliked(self):
        return self.filter(like=False)

    def rating(self):
        return self.filter(like=True).count() - self.filter(like=False).count()


class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='user')
    like = models.BooleanField(verbose_name='like')

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeDislikeManager()


class ProfileManager(models.Manager):
    def popular(self):
        return self.annotate(q_sum=Sum('question__rating'), a_sum=Sum('answer__rating')).order_by(-(F('q_sum') + F('a_sum')))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', default='uploads/teapot2.png', verbose_name='avatar')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(count=Count('question')).order_by('-count')


class Tag(models.Model):
    title = models.CharField(max_length=256, unique=True, verbose_name='title')

    objects = TagManager()

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def add_annotations(self):
        return self.annotate(num_answers=Count('answer'))

    def order_by_date(self):
        return self.add_annotations().order_by('-date_modified')

    def order_by_rating(self):
        return self.add_annotations().order_by('-rating')

    def filter_by_tag(self, tag):
        return self.add_annotations().filter(tags__title=tag).order_by('-date_modified')


class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='title')
    text = models.TextField(verbose_name='text')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name='date_modified')
    rating = models.IntegerField(default=0, verbose_name='rating')
    tags = models.ManyToManyField(Tag, blank=True)

    objects = QuestionManager()

    votes = GenericRelation(LikeDislike, related_query_name='question')

    def get_rating(self):
        return self.votes.rating()

    def save(self, *args, **kwargs):
        self.rating = self.get_rating()
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    text = models.TextField(verbose_name='text')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True, verbose_name='date_modified')
    votes = GenericRelation(LikeDislike, related_query_name='answers')
    rating = models.IntegerField(default=0, verbose_name='rating')

    def get_rating(self):
        return self.votes.rating()

    def save(self, *args, **kwargs):
        self.rating = self.get_rating()
        super(Answer, self).save(*args, **kwargs)


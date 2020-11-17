from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, LikeDislike
from django.contrib.auth.models import User
from random import choice, sample
from faker import Faker

f = Faker()

class Command(BaseCommand):
    help = 'Generate DB with python Fake'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            type=int,
            help='Indicates number of users to be created',
        )
        parser.add_argument(
            '-t',
            '--tags',
            type=int,
            help='Indicates number of tags to be created',
        )
        parser.add_argument(
            '-q',
            '--questions',
            type=int,
            help='Indicates number of questions to be created',
        )
        parser.add_argument(
            '-a',
            '--answers',
            type=int,
            help='Indicates number of answers to be created',
        )
        parser.add_argument(
            '-lq',
            '--likesdislikesquestions',
            type=int,
            help='Indicates number of likes/dislikes for questions to be created',
        )
        parser.add_argument(
            '-la',
            '--likesdislikesanswers',
            type=int,
            help='Indicates number of likes/dislikes for answers to be created',
        )

    def fill_profiles(self, cnt):
        for i in range(cnt):
            user = User.objects.create_user(
                username=f.user_name(),
                password='password12345678',
                email=f.email(),
                first_name=f.first_name(),
                last_name=f.last_name(),
            )
            Profile.objects.create(
                user=user,
                avatar='uploads/teapot3.png'
            )

    def fill_tags(self, cnt):
        for i in range(cnt):
            Tag.objects.create(
                title=f.word(),
            )

    def fill_questions(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        tag_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )

        for i in range(cnt):
            q = Question.objects.create(
                title=f.sentence()[:128],
                text=' '.join(f.sentences(f.random_int(min=2, max=5))),
                author_id=choice(author_ids),
                date_modified=f.date_time_this_month()
            )
            t = sample(tag_ids, 2)
            q.tags.add(Tag.objects.get(id=t[0]), Tag.objects.get(id=t[1]))
            q.save()

    def fill_answers(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )

        for i in range(cnt):
            Answer.objects.create(
                text=' '.join(f.sentences(f.random_int(min=2, max=5))),
                author_id=choice(author_ids),
                question_id = choice(question_ids),
                date_modified=f.date_time_this_month(),
            )

    def fill_likes_questions(self, cnt):
        user_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        likes = ('True', 'False')

        for i in range(cnt):
            q = Question.objects.get(id=choice(question_ids))
            LikeDislike.objects.create(
                user_id=choice(user_ids),
                like=choice(likes),
                content_object=q
            )
            q.save()

    def fill_likes_answers(self, cnt):
        user_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        answers_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        likes = ('True', 'False')

        for i in range(cnt):
            a = Answer.objects.get(id=choice(answers_ids))
            LikeDislike.objects.create(
                user_id=choice(user_ids),
                like=choice(likes),
                content_object=a
            )
            a.save()

    def handle(self, *args, **kwargs):
        cnt_users = kwargs['users']
        if cnt_users is not None and cnt_users != 0:
            self.fill_profiles(cnt_users)

        cnt_tags = kwargs['tags']
        if cnt_tags is not None and cnt_tags != 0:
            self.fill_tags(cnt_tags)

        cnt_questions = kwargs['questions']
        if cnt_questions is not None and cnt_questions != 0:
            self.fill_questions(cnt_questions)

        cnt_answers = kwargs['answers']
        if cnt_answers is not None and cnt_answers != 0:
            self.fill_answers(cnt_answers)

        cnt_likes_questions = kwargs['likesdislikesquestions']
        if cnt_likes_questions is not None and cnt_likes_questions != 0:
            self.fill_likes_questions(cnt_likes_questions)

        cnt_likes_answers = kwargs['likesdislikesanswers']
        if cnt_likes_answers is not None and cnt_likes_answers != 0:
            self.fill_likes_answers(cnt_likes_answers)

import datetime
import re
from django.forms import ValidationError
from django.utils import timezone
from django.db import models


def compare_alphanumeric_lower(query_string_one, query_string_two):
    # This function takes in two query strings as arguments, extracts only alphanumeric characters,
    # converts them to lowercase, and compares them
    pattern = r'\w+'
    string_one_matches = re.findall(
        pattern, query_string_one.lower())
    string_two_matches = re.findall(pattern, query_string_two.lower())
    return ''.join(string_one_matches) == ''.join(string_two_matches)


class CustomManager(models.Manager):
    def matching_alphanumeric(self, field_name, query_string):
        # This method filters a queryset based on whether the alphanumeric characters
        # of the specified field match the alphanumeric characters of the provided query string
        queryset = self.get_queryset()
        matches = []
        for obj in queryset:
            # Get the value of the specified field for the current object
            existing_string = getattr(obj, field_name)
            # If the alphanumeric characters match, append the object to the matches list
            if compare_alphanumeric_lower(existing_string, query_string):
                matches.append(obj)
        return matches


class Question(models.Model):
    # A model representing a poll question
    question_text = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('date published')

    # Define a custom manager named objects
    objects = CustomManager()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # Returns a boolean indicating whether the question was published within the last day
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def clean(self):
        # Fetch all the questions that match our current question using our custom matching algorithm
        matches = Question.objects.matching_alphanumeric(
            'question_text', self.question_text)
        if matches and matches[0].id != self.id:
            # Raise a Validation error if a question match is found and
            # the ID of the matched question does not match the ID of the current question
            raise ValidationError(
                'The question text must be unique (case-insensitive).')

    class Meta:
        # Create an index on the question_text field
        indexes = [
            models.Index(fields=['question_text']),
        ]


class Choice(models.Model):
    # A model representing a poll choice for a particular question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    objects = CustomManager()

    def __str__(self):
        return self.choice_text

    # Define a custom manager named objects
    def clean(self):
        # Fetch all the choices that match our current choice using our custom matching algorithm
        matches = Choice.objects.matching_alphanumeric(
            'choice_text', self.choice_text)
        for match in matches:
            if match.question == self.question and match.id != self.id:
                # Raise a Validation error if a choice match is found for the same question and
                # the ID of the matched choice does not match the ID of the current choice
                raise ValidationError(
                    'For a given question each choice text must be unique (case-insensitive).')

    class Meta:
        # Create an index on the choice_text field
        indexes = [
            models.Index(fields=['choice_text']),
        ]

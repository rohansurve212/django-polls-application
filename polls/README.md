<!-- @format -->

## My Approach to Part 2 of the Challenge

This part had two questions:

1. Question text must be unique, i.e., no two questions can have the same text.

2. Choice text within a question must be unique, i.e., for a given question, no two choices can have the same text.

I had a question for more clarification: How strict should the uniqueness measure be?

My solution is a result of multiple iterations.

At first, I used the **unique=True** constraint on both question_text and choice_text CharFields. However, I realized that by default, this constraint is case-sensitive, meaning that two values with different capitalization will be considered as separate values.

For example, _'Is Python fun to learn?' and 'iS python fun to learn?'_ both of these would be treated as different question texts. In my opinion, that should not be the case, should they semantically mean the same thing?

So, to ensure case-insensitive uniqueness, I tried using iexact field lookup on both question_text and choice_text. However, I then realized that my solution did not consider non-alphanumeric characters within the text. So, for example, _'Is Python fun to learn?' and 'IsPython fun to learn'_ would still be considered as different question texts, or _'Yes', 'Y e s', and 'Yes!'_ would still be considered as different choice texts.

That led me to create an algorithm that processes these input strings such that quotes, hyphens, exclamations, question marks, and other punctuation marks are disregarded when validating for duplicates.

In my final solution, I implemented a **Custom Model Manager** named CustomManager that has a custom manager method named matching_alphanumeric() that filters a queryset based on whether the alphanumeric characters of the specified field match the alphanumeric characters of the provided query string. It then raises a validation error if a corresponding match is found, and the ID of the matched object does not match the ID of the current object. I also indexed the two database tables on columns **question_text** and **choice_text** respectively to improves the speed of data retrieval operations on them.

Please check the [polls/models.py](https://github.com/rohansurve212/django-polls-application/blob/main/polls/models.py) file for the actual implementation. Thank you.

## My Solution to Part 2 of the Challenge
The [polls/models.py](https://github.com/rohansurve212/django-polls-application/blob/main/polls/models.py) file contains the solution code. I have defined a custom Django manager named CustomManager, which contains a custom method named matching_alphanumeric(). The manager is then used in the two models named Question and Choice.

The matching_alphanumeric() method takes two arguments: field_name and query_string. The method then retrieves the QuerySet for the current model instance and iterates over it. For each object in the QuerySet, the method compares the alphanumeric lowercase version of the value in the specified field_name to the alphanumeric lowercase version of the query_string. If the values match, the object is added to a list of matches, which is then returned.

Both Question and Choice models also define a clean() method that calls matching_alphanumeric() with the appropriate field name and the current object's value. If a match is found and the ID of the matched object does not match the ID of the current object, a ValidationError is raised with a message indicating that the text must be unique (case-insensitive).

The Question and Choice models both contain a CharField named question_text and choice_text, respectively, and define a custom manager **objects** that inherits from the CustomManager. They also define a DateTimeField named pub_date for Question model and an IntegerField named votes for Choice model.

Finally, the Question and Choice models both define a Meta class containing an indexes list, which specifies that an **index** should be created for the question_text and choice_text fields, respectively.

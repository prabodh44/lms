from django.db import models


# prabodh: made change to model
# prabodh: discuss about the book issues class
# prabodh: removed the author model

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_fullname = models.CharField(max_length=200)
    student_address = models.CharField(max_length=100)
    student_phone = models.CharField(max_length=100)
    student_email = models.EmailField(max_length=254, error_messages={'error': 'Please input a valid email address'})

    # TODO: add student_profile_pic to model
    # TODO: create users from the student model? (mdn-tutorial-locallibrary part 8)

    def __str__(self):
        return self.student_name


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text="Enter a brief summary")
    author = models.CharField(max_length=500)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    num_of_books = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class BookIssues(models.Model):
    # model representing specific copy of a book

    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    fine = models.PositiveIntegerField(null=True)

    def __str__(self):
        return '%s:%s' % (self.book.title, self.borrower.student_name)

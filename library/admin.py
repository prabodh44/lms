from django.contrib import admin

from library.models import Book, BookIssues, Student
# Register your models here.
admin.site.register(Book)
admin.site.register(BookIssues)
admin.site.register(Student)

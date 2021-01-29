from django.http import HttpResponse
from django.shortcuts import render, redirect
from library.models import Book, Student, BookIssues
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import F, Q

import datetime
import uuid


# first view as seen by the user
def index_view(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    if not user.is_superuser:
        student = Student.objects.get(student_name=username)
        books_borrowed = BookIssues.objects.filter(borrower__id=student.id).count()
        books_overdue = BookIssues.objects.filter(borrower__id=student.id).filter(
            due_back__lt=datetime.date.today()).count()
        books_due = BookIssues.objects.filter(borrower__id=student.id).filter(due_back=datetime.date.today()).count()
        context = {
            'books_borrowed': books_borrowed,
            'books_overdue': books_overdue,
            'books_due': books_due,
        }
    else:
        books_borrowed = BookIssues.objects.all().count()
        books_overdue = BookIssues.objects.filter(due_back__lt=datetime.date.today()).count()
        books_due = BookIssues.objects.filter(due_back=datetime.date.today()).count()
        users = User.objects.filter(is_superuser=False).filter(is_active=True).count()
        context = {
            'books_borrowed': books_borrowed,
            'books_overdue': books_overdue,
            'books_due': books_due,
            'users': users,
        }

    return render(request, "library/index.html", context)


# shows the list of all books in the library
def bookList_view(request):
    books = Book.objects.all()

    return render(request, "library/bookList.html", {'books': books})


# shows the detailed information of a single book
def bookDetail_view(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, "library/bookDetail.html", {'book': book})


# add books using a form
def addBook_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        author = request.POST["author"]
        summary = request.POST["summary"]
        num_of_books = request.POST["num_of_books"]

        book = Book.objects.create(
            title=title,
            author=author,
            summary=summary,
            num_of_books=num_of_books
        )
        book.save()
        return redirect('books')
    return render(request, "library/addBook.html", {})


# add students using a form
def addStudent_view(request):
    if request.method == "POST":
        student_name = request.POST["student_name"]
        student_fullname = request.POST["student_fullname"]
        student_password = request.POST["student_password"]
        student_address = request.POST["student_address"]
        student_phone = request.POST["student_phone"]
        student_email = request.POST["student_email"]

        # create new users
        if User.objects.filter(username=student_name).exists():
            messages.info(request, "Username already exists")
            redirect('addStudent')
        elif User.objects.filter(email=student_email).exists():
            messages.info(request, "Email already exists")
            redirect('addStudent')
        else:
            # add student to admin panel
            studentUser = User.objects.create_user(
                username=student_name,
                email=student_email,
                password=student_password,
                first_name=student_fullname,
                is_staff=True,  # creates account that does not have admin privilages
            )
            studentUser.save()

            # add student to student database
            student = Student.objects.create(
                student_name=student_name,
                student_fullname=student_fullname,
                student_address=student_address,
                student_phone=student_phone,
                student_email=student_email
            )
            student.save()

            return redirect('students')

        # if User.objects.filter(username=student_name).exists:
        #     messages.info(request, "User already exists")
        #     return redirect('addstudent')
        # elif User.objects.filter(email=student_email).exists:
        #     messages.info(request, 'Email ID already exists')
        #     return redirect('addstudent')

    return render(request, "library/addStudent.html", {})


def studentList_view(request):
    students = Student.objects.all()
    return render(request, "library/studentList.html", {'students': students})


# shows the detailed information of a single student
def studentDetail_view(request, student_id):
    student = Student.objects.get(pk=student_id)

    return render(request, "library/studentDetail.html", {'student': student})


def updateStudent_view(request, student_id):
    student = Student.objects.get(pk=student_id)
    if request.method == "POST":
        student.student_name = request.POST.get('student_name')
        student.student_fullname = request.POST.get('student_fullname')
        student.student_address = request.POST.get('student_address')
        student.student_email = request.POST.get("student_email")
        student.student_phone = request.POST.get("student_phone")
        student.save()
        return redirect('students')
    return render(request, 'library/updateStudent.html', {"student": student})


def deleteStudent_view(request, student_id):
    student = Student.objects.get(pk=student_id)
    print(student.student_name)
    try:
        studentUser = User.objects.get(username=student.student_name)
        studentUser.is_active = False
        studentUser.username = uuid.uuid4().hex[:6]  # genrate a random 6 digit alpha-numeric string
        studentUser.save()

        borrowedBooks = BookIssues.objects.filter(borrower__id=student_id)
        for borrowedBook in borrowedBooks:
            # return the books borrowed automatically
            book = Book.objects.get(pk=borrowedBook.book.id)
            print(book.num_of_books)
            book.num_of_books = F('num_of_books') + 1
            book.save()

        student.delete()

        # find the "deleted" student from the User model using the email id to reactivate
        # c = User.objects.get(email="isdu@gmail.com")
        # c.is_active = True
        # c.save()

    except User.DoesNotExist:
        print("User doesnot exist")
    return redirect('students')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                messsages.info(request, "User is inactive")
        else:
            messages.info(request, "Username or Password incorrect. Please try again")

    return render(request, "library/login.html", {})


def logout_view(request):
    logout(request)
    return redirect('login')


def updateBook_view(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.summary = request.POST.get("summary")
        book.num_of_books = request.POST.get("num_of_books")
        book.save()
        return redirect('books')
    return render(request, 'library/updateBook.html', {"book": book})


def deleteBook_view(request, book_id):
    print('book ID', book_id)
    try:
        book = Book.objects.get(pk=book_id)
    except book.DoesNotExist:
        return redirect('library/bookList')
    book.delete()
    return redirect('books')


def borrowBook_view(request, book_id, username):
    book = Book.objects.get(pk=book_id)
    student = Student.objects.get(student_name=username)
    issue_date = datetime.date.today()
    due_back = issue_date + datetime.timedelta(days=7)  # add two weeks...
    books_borrowed = BookIssues.objects.filter(borrower__id=student.id).count()

    if book.num_of_books > 0:
        if books_borrowed < 3:
            try:
                borrowed_book = BookIssues.objects.filter(borrower__id=student.id).filter(book__id=book.id)
            except BookIssues.DoesNotExist:
                print('Book does not exists')

            if (borrowed_book.count() == 0):
                bookIssue = BookIssues.objects.create(
                    book=book,
                    borrower=student,
                    issue_date=issue_date,
                    due_back=due_back,
                )
                bookIssue.save()
                books_borrowed = BookIssues.objects.filter(borrower__id=student.id).count()

                # reduce the number of books borrowed
                book.num_of_books = F('num_of_books') - 1  # F represents the value of the num_of_books_field
                book.save()
            else:
                messages.info(request, "You cannot borrow the same book twice")
        else:
            messages.info(request, "You cannnot borrow more than 3 books")
    else:
        messages.info(request, "Book is out-of-stock")
    return redirect('books')


def loanedbook_view(request):
    lBooks = BookIssues.objects.all()
    fineAdd(lBooks)

    return render(request, "library/loanedBooksList.html", {'lBooks': lBooks})


def loanedBooksByUser_view(request):
    lBooksByUser = BookIssues.objects.filter(borrower__student_name=request.user.username)
    fineAdd(lBooksByUser)
    return render(request, "library/loanedBooksByUser.html", {'lBooksByUser': lBooksByUser})


def fineAdd(books):
    for book in books:
        today = datetime.date.today()
        b = today - book.due_back
        if b.days <= 0:
            book.fine = 0
            book.save()
        if b.days >= 1 and b.days < 7:
            book.fine = 10
            book.save()
        elif b.days >= 7 and b.days < 30:
            book.fine = 20
            book.save()
        elif b.days >= 30 and b.days < 90:
            book.fine = 30
            book.save()
        elif b.days >= 90:
            book.fine = 50
            book.save()


def renewedBooksByUser_view(request):
    # try:
    #     renewBook = BookIssues.objects.filter(borrower__id=student_id).filter(book__id=book_id)
    # except renewBook.DoesNotExist:
    #     return redirect('books')
    renewBook = BookIssues.objects.all()
    return render(request, "library/renewedBooks.html", {'renewBook': renewBook})


def returnbook_view(request, student_id, book_id):
    try:
        returnbook = BookIssues.objects.filter(borrower__id=student_id).filter(book__id=book_id)
    except returnbook.DoesNotExist:
        return redirect('library/bookList')
    returnbook.delete()
    book = Book.objects.get(pk=book_id)
    book.num_of_books = F('num_of_books') + 1
    book.save()
    return redirect("loanedBook")


def renewbook_view(request, student_id, book_id):
    # try:
    renewBooks = BookIssues.objects.filter(borrower__id=student_id).filter(book__id=book_id)
    # print(renewBooks[0].due_back)
    # b = renewBooks[0].due_back + datetime.timedelta(days=7)
    # renewBooks[0].due_back = b
    # renewBooks[0].save()
    # print(renewBooks[0].due_back)
    for book in renewBooks:
        b = book.due_back + datetime.timedelta(days=7)
        book.due_back = b
        book.save()

    # except renewBooks.DoesNotExist:
    #     return redirect('library/bookList')

    return redirect("renewedBookByUser")


def searchbookbyuser_View(request):
    if request.method == "POST":
        searchString = request.POST["searchString"]
        options = request.POST["options"]
        if options == "Student":
            try:
                students = Student.objects.filter(
                    Q(student_name__icontains=searchString) | Q(student_email__icontains=searchString)
                )
                return render(request, "library/studentList.html", {'students': students})
            except students.DoesNotExist:
                return redirect('searchResult')
        else:
            try:
                books = Book.objects.filter(
                    Q(title__icontains=searchString) | Q(summary__icontains=searchString) | Q(
                        author__icontains=searchString)
                )
                return render(request, "library/bookList.html", {'books': books})
            except books.DoesNotExist:
                return redirect('searchResult')

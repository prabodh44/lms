from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index_view, name="index"),
    path('books/',views.bookList_view, name="books"),
    path('book/<int:book_id>', views.bookDetail_view, name="bookDetail"),
    path('addbook/', views.addBook_view, name="addBook"),
    path('addstudent/', views.addStudent_view, name="addStudent"),
    path('deletebook/<int:book_id>', views.deleteBook_view, name="deleteBook"),
    path('students/', views.studentList_view, name='students'),
    path('student/<int:student_id>', views.studentDetail_view, name="studentDetail"),
    path('edit/<int:student_id>', views.updateStudent_view, name="updateStudent"),
    path('deletestudent/<int:student_id>',views.deleteStudent_view, name="deleteStudent"),
    path('update/<int:book_id>', views.updateBook_view, name="updateBook"),
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout_view"),
    path('borrowBook/<int:book_id>/<str:username>',views.borrowBook_view, name="borrowBook"),
    path('loanedbook/', views.loanedbook_view,name="loanedBook"),
    path('loanedbookByUser/', views.loanedBooksByUser_view, name="loanedBookByUser"),

    path('renewedBooksByUser/', views.renewedBooksByUser_view, name="renewedBookByUser"),
    path('returnbook/<int:student_id>/<int:book_id>', views.returnbook_view, name="returnbook"),
    path('renewbook/<int:student_id>/<int:book_id>', views.renewbook_view, name="renewbook"),
    path('seachbookbyuser/',views.searchbookbyuser_View, name="searchResult")
]
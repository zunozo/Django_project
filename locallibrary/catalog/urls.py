from django.urls import path
from catalog import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/[NoReverseMatch]<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/[NoReverseMatch]<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksByUserListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/[NoReverseMatch]<int:pk>/update/', views.AuthorUpdate.as_view(),name='author_update'),
    path('author/[NoReverseMatch]<int:pk>/delete/', views.AuthorDelete.as_view(),name='author_delete'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/[NoReverseMatch]<int:pk>/update/', views.BookUpdate.as_view(),name='book_update'),
    path('book/[NoReverseMatch]<int:pk>/delete/', views.BookDelete.as_view(),name='book_delete'),
    #path('book/<uuid:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
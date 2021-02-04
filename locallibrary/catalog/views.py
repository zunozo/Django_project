import datetime
from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Author

from catalog.forms import RenewBookForm


# Create your views here.
def index(request):
    '''view function for home page of site.'''
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genre = Genre.objects.filter(name__icontains='science').count()
    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by=3
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowedBooksByUserListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    '''도서관 사서에 의해 특정 bookinstance를 갱신하는 뷰 함수.'''
    book_instance = get_object_or_404(BookInstance,pk=pk)
    # Post 요청이면 폼 데이터를 처리한다.
    if request.method == 'POST':
        #폼 인스턴스를 생성하고 요청에의한 데이터로 채운다.(binding):
        book_renewal_form = RenewBookForm(request.POST)

        #폼이 유효한지 체크한다
        if book_renewal_form.isvalid():
            # book_renewal_form.cleaned_data 데이터를 요청받은대로 처리한다.(여기선 그냥 dueback필드에 써넣는다.)
            book_inst.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_inst.save()

            #새로운 url로 보낸다.
            return HttpResponseRedirect(reverse('all-borrowed'))
    #GET 요청(혹은 다른 메소드)이면 기본 폼을 생성한다.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html',context)

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':datetime.date.today(),}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
from django.urls import path
from django.urls import include
from .views import *
from .auth import *

urlpatterns = [

    path('', index),
    #           path('login', Login),
    #           path('form', Form),
    #           path('show/<str:show_id>/',
    #                ViewShow.as_view(), name='show'),
    path('getshow/', GetShow.as_view(), name='getshow'),
    path('addsalesperson/', AddSalesperson.as_view(),
         name='addsalesperson'),
    path('getsalesperson/', getSalesperson.as_view(),
         name='getsalesperson'),
    path('addshow/', AddShow.as_view(), name='addshow'),
    path('login/', LoginView.as_view(), name='login'),
    path('check_token/', CheckToken.as_view(), name='check_token'),
    path('ticket/', TicketBook.as_view(), name='ticket'),
    path('cancelticket/', CancelTicketView.as_view(), name='cancelticket'),
    path('sales/', SalespersonTicketView.as_view(), name='clerk'),
    path('expenditure/', ExpenditureView.as_view(), name='expenditure'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
]

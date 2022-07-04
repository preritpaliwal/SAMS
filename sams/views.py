from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from .decorators import *
from django.utils.decorators import method_decorator
from datetime import datetime, timezone, timedelta
from django.db.models import Sum

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class GetShow(APIView):
    def get(self, request):
        try:
            show = Show.objects.filter(
                end_time__gte=datetime.now()).order_by('start_time')
            print(show)
            serializer = ShowSerializer(show, many=True)
            # print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddSalesperson(APIView):

    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(
                username=request.data['username'], password=request.data['password'], first_name=request.data['first_name'], last_name=request.data['last_name'])
            copy = request.data.copy()
            copy['user'] = user.id
            copy['is_salesperson'] = True
            serializer = SalespersonSerializer(data=copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class getSalesperson(APIView):
    def get(self, request):
        try:
            salesperson = Salesperson.objects.all()
            serializer = SalespersonSerializer(salesperson, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddShow(APIView):
    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):
        try:
            copy = request.data
            serializer = ShowSerializer(data=copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TicketBook(APIView):
    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):
        try:
            salesperson = Salesperson.objects.none()

            if(args[0]):
                salesperson = Salesperson.objects.filter(user=args[0]).first()
                if(not salesperson or salesperson == None):
                    return Response({"message": "only salesperson can sell tickets"}, status=status.HTTP_400_BAD_REQUEST)

            show = Show.objects.get(id=int(request.data['show']))
            numberofseat = int(request.data['numberofseat'])

            type = request.data['type']
            ticketprice = 0

            if(type == 'ORD'):
                ticketprice = show.price_ord
                if(numberofseat > show.available_ord):
                    return Response({"message": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                ticketprice = show.price_bal
                if(numberofseat > show.available_bal):
                    return Response({"message": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)
            ticket = Ticket.objects.filter(
                show=show, type=type).order_by('seat')
            # if (not ticket) and (Ticket.objects.count != 0):
            #     return Response({"message": "No tickets available"}, status=status.HTTP_400_BAD_REQUEST)
            
            intialseat = 1
            totaldata = []
            n = len(ticket)
            for num in range(0, numberofseat):
                while intialseat-1-num < n:
                    item = ticket[intialseat-1-num]
                    print(item.seat, intialseat)
                    if(item.seat != intialseat):
                        break
                    intialseat = intialseat+1

                salescommission = salesperson.percent_commission*ticketprice*0.01
                salesperson.amount_collected = salesperson.amount_collected+ticketprice
                salesperson.total_commission = salesperson.total_commission+salescommission
                newticket = Ticket.objects.create(
                    show=show, type=type, seat=intialseat, salesperson=salesperson, name=request.data['name'], email=request.data['email'], price=ticketprice, salescommission=salescommission)
                print(newticket)
                newticket.save()
                totaldata.append(newticket)
                if(type == 'ORD'):
                    show.available_ord = show.available_ord-1
                    show.save()
                else:
                    show.available_bal = show.available_bal-1
                    show.save()
                intialseat = intialseat+1
            trans=Transaction(desc='ticket Booked',amount=ticketprice*numberofseat,transaction_type='credit')
            trans.save()
            salesperson.save()
            serializer = TicketSerializer(totaldata, many=True)

            return Response({"data": serializer.data, "message": "ticket booked successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CancelTicketView(APIView):
    @method_decorator(unauthenticated_user)
    def delete(self, request, *args, **kwargs):
        try:

            showname = request.data['showname']
            type = request.data['type']
            show = Show.objects.filter(name=str(showname)).first()
            print(show)
            if(not show):
                return Response({"message": "show not found"}, status=status.HTTP_400_BAD_REQUEST)
            ticket = Ticket.objects.filter(
                name=request.data['name'], email=request.data['email'], show=show, seat=int(request.data['seat']), type=request.data['type']).first()
            if(not ticket):
                return Response({"message": "ticket not found"}, status=status.HTTP_400_BAD_REQUEST)
            salesperson = ticket.salesperson
            salesperson.total_commission = salesperson.total_commission-ticket.salescommission
            amount_to_return = 0
            # print(show.start_time,datetime.now(timezone.utc))
            timediff = show.start_time-datetime.now(timezone.utc)
            print(timediff)
            if(timediff < timedelta(0)):
                return Response({"message": "cannot cancel ticket after show start"}, status=status.HTTP_400_BAD_REQUEST)
            if timediff >= timedelta(days=3):
                amount_to_return = ticket.price-5
                salesperson.amount_collected = salesperson.amount_collected-amount_to_return
            elif timediff > timedelta(days=1) and timediff < timedelta(days=3):
                if(type == 'ORD'):
                    amount_to_return = ticket.price-10
                else:
                    amount_to_return = ticket.price-15
                salesperson.amount_collected = salesperson.amount_collected-amount_to_return
            else:
                amount_to_return = ticket.price/2
                salesperson.amount_collected = salesperson.amount_collected-amount_to_return

            if(ticket):
                trans=Transaction(amount=amount_to_return,transaction_type='debit',desc='ticket cancelled')
                salesperson.save()
                
                ticket.delete()
                if(type == 'ORD'):
                    show.available_ord = show.available_ord+1
                    show.save()
                else:
                    show.available_bal = show.available_bal+1
                    show.save()
                return Response({"message": "ticket cancelled successfully", "amount_to_return": amount_to_return, "price": ticket.price}, status=status.HTTP_200_OK)
            return Response({"message": "ticket not found"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SalespersonTicketView(APIView):
    @method_decorator(get_protection)
    def get(self, request, *args, **kwargs):
        try:
            user = args[0]
            sales = Salesperson.objects.filter(user=user).first()
            if(not sales):
                return Response({"message": "salesperson not found"}, status=status.HTTP_400_BAD_REQUEST)
            ticket = sales.ticket_set.all()
            ticket_count = ticket.count()
            sales = SalespersonSerializer(sales)

            data = sales.data
            data['ticket_count'] = ticket_count
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExpenditureView(APIView):
    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):
        try:
            user = args[0]
            clerk = Clerk.objects.filter(user=user).first()
            if(not clerk):
                return Response({"message": "only clerk can add expenditure"}, status=status.HTTP_400_BAD_REQUEST)
            showname = request.data['showname']
            show = Show.objects.filter(name=str(showname)).first()
            if(not show):
                return Response({"message": "show not found"}, status=status.HTTP_400_BAD_REQUEST)
            copy = request.data.copy()
            copy['show'] = show.id
            exp = ExpenditureSerializer(data=copy)
            
            if exp.is_valid():
                trans=Transaction(amount=request.data['amount'],transaction_type=request.data['transaction_type'],desc=request.data['desc'])
                trans.save()
                exp.save()
                return Response({"message": "expenditure added successfully"}, status=status.HTTP_201_CREATED)

            return Response({"message": "some error occurred"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClerkView(APIView):
    @method_decorator(get_protection)
    def get(self, request, *args, **kwargs):
        try:
            # user = args[0]
            # if(user.type != 'clerk'):
            #     return Response({"message": "only clerk can view expenditure"}, status=status.HTTP_400_BAD_REQUEST)
            show = Show.objects.all()
            showdata = []
            for item in show:
                ticket = item.ticket_set.all()
                ticketcount = ticket.count()
                amount = ticket.aggregate(Sum('price'))['price__sum']
                name = item.name
                showdata.append({name, ticket, amount})
            ticketcount = Ticket.objects.count()
            salesperson = Salesperson.objects.all()
            amount = salesperson.aggregate(Sum('amount_collected'))
            data = {}
            data['ticketcount'] = ticketcount
            data['amount'] = amount['amount_collected__sum']
            data['showdata'] = showdata
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransactionView(APIView):
    @method_decorator(get_protection)
    def get(self, request, *args, **kwargs):
        try:
            # user = args[0]
            # if(user.type != 'manager'):
            #     return Response({"message": "only manager can view expenditure"}, status=status.HTTP_400_BAD_REQUEST)
            trans=Transaction.objects.all()
            print(trans,"hiii")
            if(not trans):
                return Response()
            serializer=TransactionSerializer(trans,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            
        


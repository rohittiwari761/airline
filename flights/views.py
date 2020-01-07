from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import flight,Airport,passenger
# Create your views here.
def index(request):
    context={
    'flights':flight.objects.all()
    }

    return render(request,'flights/index.html',context)
def Flight(request,flight_id):
    try:
        Flight=flight.objects.get(id=flight_id)
    except flight.DoesNotExist:
        raise Http404('Flight does not exist')

    context={
        'flight':Flight,
        'passenger':Flight.passenger.all(),
        'non_passenger':passenger.objects.exclude(flights=Flight).all()
    }
    return render(request,'flights/flight.html',context)
def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        flights = flight.objects.get(pk=flight_id)
        passengers = passenger.objects.get(pk=passenger_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection."})
    except flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No flight."})
    except passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No passenger."})
    passengers.flights.add(flights)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

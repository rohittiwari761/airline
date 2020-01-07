from django.test import Client, TestCase

# Create your tests here.
from .models import Airport,flight,passenger

class ModelsTestCase(TestCase):
    def setUp(self):
        a1 =Airport.objects.create(code='AAA',city='city A')
        a2 =Airport.objects.create(code='BBB',city='city B')


        flight.objects.create(origin=a1,destination=a2,duration=100)
        flight.objects.create(origin=a1,destination=a1,duration=200)
        flight.objects.create(origin=a1,destination=a2,duration=-100)
    def test_departure(self):
        a=Airport.objects.get(code='AAA')
        self.assertEqual(a.departure.count(), 3)

    def test_arrival_count(self):
        a=Airport.objects.get(code="AAA")
        self.assertEqual(a.arrival.count(),1)

    def test_valid_flight(self):
        a1=Airport.objects.get(code='AAA')
        a2=Airport.objects.get(code='BBB')
        f =flight.objects.get(origin=a1,destination=a2,duration=100)
        self.assertTrue(f.is_valid_flight())


    def test_invalid_flight_destination(self):
        a1=Airport.objects.get(code='AAA')
        f=flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c=Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flights'].count(), 3)


    def invalid_duration(self):
        a1=Airport.objects.get(code='AAA')
        a2=Airport.objects.get(code='BBB')
        flight.objects.create(origin=a2,destination=a1,duration=-100)
        self.assertFalse(f.is_valid_flight())

    def valid_flight(self):
        a1=Airport.objects.get(code='AAA')
        f=flight.objects.get(origin=a1,destination=a1)
        c=Client()
        response=c.get(f'/{f.id}')
        self.assertEqual(response.status_code,200)

    def invalid_flight_page(self):
        max_id=flight.objects.all().aggregate(Max('id'))['id_max']
        c= Client
        response= c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code,400 )

    def test_passenger(self):
        f=flight.objects.get(pk=1)
        p=passenger.objects.create(first='Alice',last='Adam' )
        f.passenger.add(p)
        c=Client()
        response=c.get(f'/{f.id}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['passenger'].count(), 1 )


    def test_no_passenger(self):
        f=flight.objects.get(pk=1)
        p=passenger.objects.create(first='Alice', last='Adam' )

        c=Client()
        response=c.get(f'/{f.id}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['non_passenger'].count(), 1 )

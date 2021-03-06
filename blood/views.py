from django.shortcuts import render
from .models import Location, Profile
# Create your views here.
from math import sin, cos, sqrt, atan2, radians, degrees, sin, cos, radians, degrees, acos



from django.contrib.auth.models import User, auth


import requests

from django.views.decorators.csrf import csrf_exempt


key = "0f9f6b4b15d7c900a25be24e309d5b99"

#twilio
from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from twilio.rest import Client


def home(request):

    data = Location.objects.all()

    prof = Profile.objects.all()

    ls = []
    temp={}
    for x in prof:
        temp={}
        temp['name'] = x.name
        temp['contact'] = x.contact
        temp['address'] = x.address

        ip = x.ip

        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        response = requests.get(url).json()
        print(response)
        lat = response['latitude']
        lon = response['longitude']

        temp['latitude'] = lat
        temp['longitude'] = lon

        ls.append(temp)

    print(ls)
    return render(request, 'index.html',{'data': ls} )

@csrf_exempt
def search(request):

    print("hello")
    
    radius = 10000
    car = '1'
    if request.method == "POST":
        radius = int(request.POST['radius'])*10000

        car = request.POST['radius']


    user_lat = radians(19.1778797)
    user_lon = radians(72.8733183)

    data = Profile.objects.all()

    R = 6373.0

    # lat1 = radians(52.2296756)
    # lon1 = radians(21.0122287)

    ls = []
    print(radius)
    for x in data:
        lat_user = radians(19.1778797)
        ip = x.ip
        key = "0f9f6b4b15d7c900a25be24e309d5b99"
        print("hi")
        # print(x.ip)
        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        
        response = requests.get(url).json()
        # print(response)
        lat = response['latitude']
        lon = response['longitude']

        lat_b = radians(lat)
        long_diff = radians(72.8733183 - lon)
        distance = (sin(lat_user) * sin(lat_b) +
                    cos(lat_user) * cos(lat_b) * cos(long_diff))
        resToMile = degrees(acos(distance)) * 69.09
        resToMt = resToMile / 0.00062137119223733

        # print(resToMt)

        if resToMt < radius:
            temp={}
            temp['name'] = x.name
            temp['contact'] = x.contact
            temp['address'] = x.address

            ip = x.ip

            temp['latitude'] = lat
            temp['longitude'] = lon

            temp['id'] = x.id

            temp['bloodgroup'] = x.bloodgroup

            ls.append(temp)
                
    print(ls)

    #BLOOD Banks
    
    print(car)
    return render(request, 'map.html',{'data': ls, 'rad': radius, 'temp':car, } ) 


def register(request):

    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        ip = request.POST['ip']
        username = request.POST['username']
        password =request.POST['password']
        bloodgroup = request.POST['bloodgroup']
        print(name)
        print(ip)

           
        key = "0f9f6b4b15d7c900a25be24e309d5b99"
        
        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        response = requests.get(url).json()
        print(response)
        lat = response['latitude']
        lon = response['longitude']

        loc = Location.objects.create(latitude= lat, longitude=lon)
        user = User.objects.create_user(username = username, password = password )
        user.save()
        loc.save()
        Profile.objects.create(bloodgroup = bloodgroup, name = name, contact = contact, address = address, location=loc, ip = ip, user=user)

        return render(request, 'logindonor.html')

    return render(request, 'register.html')    


def sms(request):
    message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                "yet? Grab it here: https://www.twilio.com/quest")
    client = Client("AC9d8a94f846d748f362e6dda727e83eaa", "45c894517cded405080dcb9984c9ce27")
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   from_="+14422426473",
                                   body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)

def login(request):
    if request.method == "POST":
        
        username = request.POST['username']
        password =request.POST['password']
        
        user =  auth.authenticate(username=username,password=password)
        print(user)
        try:
            
            auth.login(request, user)
            return render(request, 'index.html')
        except:
            print("error")
            pass

    return render(request, 'logindonor.html')  

def mydata(request):

    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        bloodgroup = request.POST['bloodgroup']
        username = request.user.username

        Profile.objects.filter(user__username=username).update(bloodgroup = bloodgroup, name = name, contact = contact, address = address)
        

        return render(request, 'index.html')
        
    z = User.objects.filter(username=request.user.username)

    print(z)
    data = Profile.objects.get(user = z[0])
    
    
    return render(request, 'mydata.html', {'data':data})    

def emergency(request):

    if request.method=="POST":
        message = request.POST['message']
        ip = request.POST['ip']

        key = "0f9f6b4b15d7c900a25be24e309d5b99"
        # print("hi")
        # print(x.ip)
        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        
        response = requests.get(url).json()
        # print(response)
        lat_user = response['latitude']
        lon_user = response['longitude']
        print(lat_user)
        print(lon_user)
        from opencage.geocoder import OpenCageGeocode
        key = '8c0d6897d5334facb9c5419400ff2dab'

        geocoder = OpenCageGeocode(key)

        results = geocoder.reverse_geocode(lat_user, lon_user )
        print(results[0]['formatted'])
        add = results[0]['formatted']
        message = message + "Address- " + add
        radius = 10000
        car = 1
        user_lat = radians(response['latitude'])
        user_lon = radians(response['longitude'])

        data = Profile.objects.all()

        R = 6373.0

        
        ls = []
        print(radius)
        for x in data:
            lat_user = radians(19.1778797)
            ip = x.ip
            key = "0f9f6b4b15d7c900a25be24e309d5b99"
            print("hi")
            # print(x.ip)
            url = "http://api.ipstack.com/" + ip +"?access_key=" + key
            
            response = requests.get(url).json()
            # print(response)
            lat = response['latitude']
            lon = response['longitude']

            lat_b = radians(lat)
            long_diff = radians(72.8733183 - lon)
            distance = (sin(lat_user) * sin(lat_b) +
                        cos(lat_user) * cos(lat_b) * cos(long_diff))
            resToMile = degrees(acos(distance)) * 69.09
            resToMt = resToMile / 0.00062137119223733

            # print(resToMt)

            if resToMt < radius:
                temp={}
                temp['name'] = x.name
                temp['contact'] = x.contact
                temp['address'] = x.address

                ip = x.ip

                temp['latitude'] = lat
                temp['longitude'] = lon

                temp['id'] = x.id

                temp['bloodgroup'] = x.bloodgroup

                ls.append(temp)
                    
        print(ls)
        
        print(car)

        contact_list = []

        for x in ls:
            temp = "+"+str(x['contact'])
            contact_list.append(temp)
            print(x['contact'])

        message_to_broadcast = (message)
        client = Client("AC9d8a94f846d748f362e6dda727e83eaa", "ec46f7a3a849a73af6db6874516a2c3b")
        for recipient in contact_list:
            if recipient:
                client.messages.create(to=recipient,
                                    from_="+14422426473",
                                    body=message_to_broadcast)

        return render(request, 'emergencymap.html', {"data": ls, 'rad': radius, 'temp':car})
        

    return render(request, 'emergencyform.html')    


def compatibility(request):
    return render(request, 'compatibility.html')    
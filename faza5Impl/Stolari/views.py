from django.http import HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin, Menadzer, Registrovani, Galerija, Objekat, Omiljeni
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings
from django.urls import reverse


def login(request): #login logika - Pavle Perovic 0594/14
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if Admin.objects.filter(username=username, password=password).exists():
            request.session['username'] = username
            return render(request, 'admin.html')
        elif Menadzer.objects.filter(username=username, password=password).exists():
            request.session['username'] = username
            return render(request, 'menadzer.html')
        elif Registrovani.objects.filter(username=username, password=password).exists():
            request.session['username'] = username
            return render(request, 'userIndex.html')
        else:
            poruka = "Pogresan username ili password"
            return render(request, 'login.html', {'poruka': poruka, 'template_name': 'login.html'})
    else:
        return render(request, 'login.html', {'template_name': 'login.html'})

def logout_view(request): #logout logika - Pavle Perovic
    logout(request) #logout radi i flush i modified = true
    return redirect('login') #skoci na pocetnu stranu

def register_render(request): #hendler za redirect - Pavle Perovic
    return render(request, 'register.html')

def register(request): #registracija korisnika - Pavle Perovic
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        number = request.POST.get('number')
        gender = request.POST.get('gender')
        datetime = request.POST.get('datetime')

        if username is None or password is None or first_name is None or last_name is None or number is None or gender is None or datetime is None:
            error = 'Neispravan unos!'
            return render(request, 'register.html', {'error': error})
        if username.strip() == '' or password.strip() == '' or first_name.strip() == '' or last_name.strip() == '' or number.strip() == '' or gender.strip() == '' or datetime.strip() == '':
            error = 'Sva polja moraju biti popunjena!'
            return render(request, 'register.html', {'error': error})
        #Obrada unique podataka.
        if Registrovani.objects.filter(username=username).exists():
            error = 'Username vec postoji!'
            return render(request, 'register.html', {'error': error})
        if Registrovani.objects.filter(brtelefona=number).exists():
            error = 'Broj telefona vec postoji!'
            return render(request, 'register.html', {'error': error})

        # Insert
        user = Registrovani(username=username, password=password, ime=first_name, prezime=last_name, brtelefona=number, pol=gender, datumrodjenja=datetime, pozpoeni=0, negpoeni=0)
        user.save()

        # Redirektujemo se na pocetnu stranicu
        return redirect('login')

    # ako metoda nije POST
    error = 'Metoda nije POST!'
    return render(request, 'register.html', {'error': error})



def user_profile_view(request):
    username = request.session.get('username')
    if not username:
        redirect('login')
    user = Registrovani.objects.get(username=username)
    context = {
        'first_name': user.ime,
        'last_name': user.prezime,
        'phone_number': user.brtelefona,
        'points': user.pozpoeni - user.negpoeni
    }
    return render(request, 'userProfile.html', context)



def explore_render(request): #hendler za redirect
    return render(request, 'explore.html')

def prikaziExplore(request):
    objekti = Objekat.objects.all()
    context = {'objekti': objekti}
    return render(request, 'explore.html',context)

@require_http_methods(["POST"])
def prikaziStranicuObjekta(request,idobj):
    if request.method=="POST":
        objekat=get_object_or_404(Objekat,idobj=idobj)
        context = {'objekat': objekat}
        return render(request, 'stranicaObjekta.html', context)
    error='Metoda nije POST!'
    return render(request, 'register.html', {'error':error})


@require_http_methods(["POST"])
def add_favorites(request, idobj):
    if request.method != 'POST':
        return HttpResponseBadRequest('Samo POST zahtevi su podržani')

    username = request.session.get('username')

    try:
        user = Registrovani.objects.get(username=username)
    except Registrovani.DoesNotExist:
        return Http404('Morate biti registrovan korisnik.')

    omiljen_obj= Omiljeni.objects.filter(idrreg=user.idrreg,idobj=idobj).first()
    if(omiljen_obj==None):
            omiljen_obj = Omiljeni(idrreg=user.idrreg,idobj=idobj)
            omiljen_obj.save()
            return HttpResponse('Objekat je dodat u omiljene.')
    else:
        return HttpResponse('Objekat je vec u omiljenima.')

@require_http_methods(["POST"])
def delete_favorites(request, idobj):
    if request.method != 'POST':
        return HttpResponseBadRequest('Samo POST zahtevi su podržani')

    username = request.session.get('username')

    try:
        user = Registrovani.objects.get(username=username)
    except Registrovani.DoesNotExist:
        return Http404('Morate biti registrovan korisnik.')

    omiljen_obj= Omiljeni.objects.filter(idrreg=user.idrreg,idobj=idobj).first()
    if(omiljen_obj!=None):
            omiljen_obj.delete()
            return HttpResponse('Objekat je obrisan iz omiljenih..')
    else:
        return HttpResponse('Objekat nije ni bio u omiljenima.')

def prikaziOmiljene(request):
    username=request.session.get('username')
    korisnik = get_object_or_404(Registrovani, username=username)
    korisnik_id=korisnik.idrreg
    try:
        objekti_id = Omiljeni.objects.filter(idrreg=korisnik_id).values_list('idobj', flat=True)
        objekti = Objekat.objects.filter(idobj__in=objekti_id)
    except Omiljeni.DoesNotExist:
        objekti=[]
    context = {'objekti': objekti}
    return render(request, 'omiljeni.html',context)

@require_http_methods(["POST"])
def oceni_objekat(request,idobj):
    if request.method == "POST":
        objekat = get_object_or_404(Objekat, idobj=idobj)
        ocena = int(request.POST.get('rating'))
        objekat.ukocena+=ocena
        objekat.brocena+=1
        objekat.save()
        return HttpResponse("Objekat je ocenjen.")
    else:
        return HttpResponse("Došlo je do greške. Za ocenu objekta koristite POST metodu.")

@require_http_methods(["POST"])
def reservePlace(request,idobj):
    if request.method == "POST":
        objekat = get_object_or_404(Objekat, idobj=idobj)
        context={
            'objekat':objekat
        }
        return render(request,'reservePlace.html',context)
    else:
        return HttpResponse("Došlo je do greške.")


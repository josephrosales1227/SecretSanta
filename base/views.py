from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Group, Relation
import random
import string

# Create your views here.
def deleteGroup(request, code):
    group = Group.objects.get(code=code)
    if request.method == 'POST':
        group.delete()
        return redirect('/')
    return render(request, 'delete-group.html', {'name':group.name})

def drawName(request, code):
    context = {}
    if request.method == 'POST':
        individualCode=request.POST.get('personCode')
        Relation.objects.get(individualCode=individualCode, groupCode=code)
        return redirect('getPerson', groupCode=code, individualCode=individualCode)
    if Group.objects.filter(code=code).exists():
        print('here')
        group = Group.objects.get(code=code)
        context['group'] = group
    else:
        return redirect('/')
    return render(request, 'draw-name.html', context)

def getPerson(request, groupCode, individualCode):
    group = Group.objects.get(code=groupCode)
    data = Relation.objects.get(individualCode=individualCode, groupCode=groupCode)
    return render(request, 'get-person.html', {'group':group, 'data':data})

@login_required(login_url='loginPage')
def account(request):
    groups = Group.objects.filter(host=request.user)
    context = {'groups': groups}
    return render(request, 'account.html', context)

def createAccount(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            redirect('/')
        else:
            messages.error(request, 'Could not create account')
    return render(request, 'create-account.html', {'form': form})

@login_required(login_url='loginPage')
def newGroup(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('groupName')
            numberOfParticipants = int(request.POST.get('numParticipants'))
            budget = int(request.POST.get('budget'))
        except:
            messages.error(request, 'Could not create group')
            return redirect('/')
        if (budget > 0) and (name != '') and (numberOfParticipants > 3):
            return redirect('addParticipants', groupName=name, numParticipants=numberOfParticipants, budget=budget)
        else:
            messages.error(request, 'Could not create group')
            return redirect('/')
    return render(request, 'new-group.html')

def reveal(request):
    return render(request, 'reveal.html')

@login_required(login_url='loginPage')
def viewGroup(request, code):
    group = Group.objects.get(code=code)
    participants = Relation.objects.all().filter(groupCode=code)
    if request.user != group.host:
        return HttpResponse('You are not this groups host')
    return render(request, 'view-group.html', {'group': group, 'participants':participants})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {}
    return render(request, 'loginpage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def addParticipants(request, groupName, numParticipants, budget):
    numParticipants = int(numParticipants)
    budget = int(budget)
    ls = []
    for num in range(1, numParticipants + 1):
        ls.append(num)

    if request.method =='POST':
        giver = []
        usedCodes = set()
        for num in ls:
            personName = request.POST.get('person' + str(num))
            if personName == '':
                messages.error(request, 'Could not create account')
                return redirect('/')
            giver.append(personName)
        group = Group.objects.create (
                host = request.user,
                name = groupName,
                numberOfParticipants = numParticipants,
                budget = budget
            )
        random.shuffle(giver)
        receiver = giver.copy()
        first = receiver[0]
        last = len(receiver)
        for index, name in enumerate(receiver):
            if index == last - 1:
                break
            receiver[index] = receiver[index + 1]
        receiver[last - 1] = first
        for index, giverName in enumerate(giver):
            code = ''
            while True:
                code = ''.join(random.choices(string.ascii_uppercase, k=6))
                if code not in usedCodes:
                    usedCodes.add(code)
                    break
            Relation.objects.create (
            groupCode = group,
            giver = giverName,
            receiver = receiver[index],
            individualCode = code
        )   
        return redirect('/')
    return render(request, 'add-participants.html', {'list' : ls})
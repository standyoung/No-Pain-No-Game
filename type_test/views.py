import json

from django.shortcuts import render
from django.forms import model_to_dict


# Create your views here.
from account.models import User


def type_test(request):
    authuser = request.session.get('authUser')
    if request.method == 'POST':
        j = request.POST['type_id']
        u = User.objects.get(member_id=authuser['member_id'])
        u.type_id = j
        u.save()
        results = User.objects.filter(member_id=authuser['member_id'])
        authUser = results[0]
        request.session['authUser'] = model_to_dict(authUser)
        return render(request, 'type_test/type_test.html')
    else:
        return render(request, 'type_test/type_test.html')


def type_1(request):
    return render(request, 'type_result/type_1.html')


def type_2(request):
    return render(request, 'type_result/type_2.html')


def type_3(request):
    return render(request, 'type_result/type_3.html')


def type_4(request):
    return render(request, 'type_result/type_4.html')
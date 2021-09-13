import random
import string
from django.shortcuts import render
from django.http import HttpResponse, response
from django.shortcuts import render
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from onlinec.settings import BASE_DIR
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser, User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from userapp.models import saveddata
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# from onlinec.customauth import CsrfExemptSessionAuthentication
from django.contrib.auth.decorators import login_required
# Create your views here.
import os
@login_required
def index(request):
    print(request.user.is_authenticated)
    # return HttpResponse("hello world")
    return render(request, "capp/index2.html")

def indexguest(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "capp/indexguest.html")

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginview'))



class inprun(APIView):
    # permission_classes = ()
    # authentication_classes = ()
    # authentication_classes = (CsrfExemptSessionAuthentication)
    def post(self, request):
        def random_string_generator(str_size, allowed_chars):
            return ''.join(random.choice(allowed_chars) for x in range(str_size))        
        chars = string.ascii_lowercase + string.digits    
        # cmdl = request.data["cmdl"]
        code = request.data["code"]
        # inp = ""
        fname = "a"+random_string_generator(15, chars)        
        a = 1
        # for c in cmdl:
        #     if a==1:
        #         inp = str(c)
        #         a = 0
        #         continue
        #     inp = inp +"\n"+ str(c)
        inp = request.data["input"]
        fnamefull = "./temp2/"+fname+".cpp" 
        fnamefull = fname+".cpp" 
        f = open(fnamefull, "w")
        f.write(code)
        f.close()

        cmd1 = "g++ "+fnamefull+" -o "+fname 
        a = subprocess.run(cmd1, shell=True, capture_output=True)
        # op = a.stdout.decode()
        if a.returncode !=0:
            os.remove(fnamefull)
            op = a.stderr.decode()
            msg = {
                "resp": "fail",
                "output": op
            }
            return Response(msg)
        
        try:
            a2 = subprocess.run("./"+fname,timeout=5, shell=True, capture_output=True,input=inp.encode())
            print("done")
            os.remove(fnamefull)
            # os.remove(fname + ".exe")
            os.remove(fname)
        except subprocess.TimeoutExpired:
            msg = {
                "resp": "success",
                "output": "Timeout this may be caused by infinite loop in program"
            }
            return Response(msg)
            
        op = a2.stdout.decode()
        op = op + a2.stderr.decode()
        print("four")
        msg = {
            "resp": "success",
            "output": op
        }
        return Response(msg)

def loginview(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capp/login.html", {
                "message": "Invalid username and/or password."
        })
    
    else:
        if request.user.is_authenticated:
            
            return HttpResponseRedirect(reverse("index"))
        return render(request,"capp/login.html")
 

def registerview(request):
    if request.method == "POST":
        username = request.POST["username"]
        # email = request.POST["email"]
        # username = username.replace(" ", "")
        # print(username)
        # return HttpResponseRedirect(reverse("indexguest"))
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        email = ""
        if password != confirmation:
            return render(request, "capp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            
            return HttpResponseRedirect(reverse("index"))
        return render(request, "capp/register.html")

class savefile(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        code = request.data["code"]
        fname = request.data["filename"]
        fname = " ".join(fname.split())
        mode = request.data["mode"]
        if saveddata.objects.filter(user=request.user, file_name = fname).exists():
            if mode == "alreadyexist":
                f = saveddata.objects.get(user=request.user, file_name = fname)
                f.code = code
                f.save()
                msg ={
                    "resp":"successful",
                }
                return Response(msg,status=status.HTTP_200_OK)
            msg = {
                "resp": "fail",
                "msg":"File with the same name already exist"
            }
            return Response(msg, status=status.HTTP_226_IM_USED)
        a = saveddata(user = request.user, code=code, file_name=fname)
        a.save()
        msg ={
            "resp":"successful",
        }
        return Response(msg,status=status.HTTP_200_OK)

@login_required    
def showfile(request, filename):
    f = saveddata.objects.get(user = request.user, file_name = filename)
    return render(request, "capp/showfile.html",{
        "code":f.code,
        "fname":f.file_name
    })

@login_required   
def allflesview(request):
    f = saveddata.objects.filter(user = request.user)

    return render(request, "capp/allfiles.html",{
        "li":f
    })
    

# not in use
def runz(request):

    c = request.data["code"]

    def random_string_generator(str_size, allowed_chars):
        return ''.join(random.choice(allowed_chars) for x in range(str_size))

    chars = string.ascii_letters + string.punctuation
    size = 12
    fname = BASE_DIR+"/temp2/"+random_string_generator(size, chars) + ".cpp"
    f = open(fname, "w")
    f.write(c)
    f.close()

    cmd = "g++ "+fname+".cpp"
    a = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    cmd2 = fname
    a2 = subprocess.run(cmd2, shell=True, stdout=subprocess.PIPE)
    print(a2.stdout.decode)

    # print(a)
    # print(chars)
    # print('Random String of length 12 =', random_string_generator(size, chars))
    # st =

    return HttpResponse("successfull")


class runb(APIView):

    def post(self, request):
        c = request.data["code"]

        def random_string_generator(str_size, allowed_chars):
            return ''.join(random.choice(allowed_chars) for x in range(str_size))

        chars = string.ascii_letters + string.punctuation
        size = 12
        # fname = random_string_generator(size, chars) + ".cpp"
        # fname2 = "one"
        chars = string.ascii_lowercase + string.digits
        fname2 = "a"+random_string_generator(15, chars)
        fname = "temp2/"+fname2 + ".cpp"
        f = open(fname, "w")
        f.write(c)
        f.close()

        cmd = "g++ "+fname+" -o " + fname2

        a = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, input="")
        if a.returncode != 0:
            op = str(a.stderr.decode())
            msg = {
                "resp": "success",
                "output": op
            }

            return Response(msg)

        cmd2 = fname2
        a2 = subprocess.run(
            cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # f2 = open("f2.txt", "w")
        # f2.write(str(a2.stdout.decode()))
        # f2.close
        op = str(a2.stdout.decode())

        print(str(a2.stdout.decode()))

        # print(a)
        # print(chars)
        # print('Random String of length 12 =', random_string_generator(size, chars))
        # st =
        msg = {
            "resp": "success",
            "output": op
        }
        return Response(msg)


class checkusername(APIView):
    def post(self,request):
        username = request.data["username"]
        if User.objects.filter(username = username).exists():
            return Response({"resp":"not-available"}, status=status.HTTP_226_IM_USED)
        else:
            return Response({"resp":"available"}, status=status.HTTP_200_OK)

class deletefile(APIView):
    def post(self,request):
        fname = request.data["filename"]
        saveddata.objects.get(user = request.user, file_name = fname).delete()
        return Response({"resp":"sucess"}, status=status.HTTP_200_OK)

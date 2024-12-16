from django.shortcuts import render,redirect

from django.views.generic import View

from task.forms import SignUpForm,SignInForm,TodoForm

from django.contrib.auth import authenticate,login,logout

from task.models import Todo

from django.utils.decorators import method_decorator

from task.decorators import signin_required

from django.views.decorators.cache import never_cache


# Create your views here.

#step1:=>
#django.contrib.auth.models
#AbstractBaseUser(password)
#AbstractUser(f_name,l_name,e_mail)
#User(abstractUser)

#step2:
#register custom user model

#step3:
#AUTH_USER_MODEL="task.User"  settings.py

decs=[signin_required,never_cache]

class SignUpView(View):

    template_name="signup.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.save()

            print("account created")

            return redirect("signup")
        
        print("failed")
        
        return render(request,self.template_name,{"form":form_instance})
    
#SignIn

class SignInViews(View):

    template_name="signin.html"

    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pswd=data.get("password")

            user_object=authenticate(request,username=uname,password=pswd)

            if user_object:
                
                login(request,user_object)

                print("session started")

                return redirect("index")

            print("invalid credential")

            return render(request,self.template_name,{"form":form_instance})

#logout

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        print("session ended")

        return redirect("signin")
    
#todo .....todo create list update =>index


@method_decorator(decs,name="dispatch")
class IndexView(View):

    template_name="index.html"

    form_class=TodoForm

    def get(self,request,*args,**kwargs):

        #login user of todo

        qs=Todo.objects.filter(owner=request.user)

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            #form_instance.save() #error todo.owner is missing
                     
                     #data=form_instance.cleaned_data
                     #Todo.objects.create(**data)

                               ## OR ##
                    #form_instance=>todoform
                    #form_instance.    instance =>from modelform
                    #value to form_instance.instance=>owner=request.user
                    
            return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})


#delete

@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Todo.objects.get(id=id).delete()

        return redirect("index")
    
#update

@method_decorator(decs,name="dispatch")
class TodoUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Todo.objects.filter(id=id).update(status=True)

        return redirect("index")


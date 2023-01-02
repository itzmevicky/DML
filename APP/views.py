from django.shortcuts import render,redirect,get_object_or_404
from .models import PostCount,PostLikeBy
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
from django.contrib import messages


def loginView(request): 
    data = dict()
    if request.method == 'POST':        
        un = request.POST.get('username')
        pwd = request.POST.get('password')
        if un and pwd:
            user = authenticate(username=un,password=pwd)                       
            if user:
                login(request,user)                
                return redirect('/')
            messages.error(request,'Invalid Login Credentials')
            
    return render(request,'login.html',context=data)

def Register(request):    
    form = RegisterUser()
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created Successfully...')           
            return redirect('/login')        
    return render(request,'register.html',{'form':form})

def home(request):
    if request.user.is_authenticated:          
        postInst = PostCount.objects.get(id=1)
        userInst = getpostby(PostLikeBy,request.user.id)
        if postInst:
            context = {
                'likes':postInst.like,
                'dislikes':postInst.dislike,
            } 
        if userInst:
            context['isliked'] = userInst.like
            context ['isdliked'] = userInst.dislike
        else:
            context['isliked'] = 0
            context ['isdliked'] = 0

        return render(request,'home.html',context=context)        
    return redirect('/login')   
 
def logoutView(request):
    logout(request)
    return redirect('/login')  
   
def dlikeView(request):
    userInst = None
    totallike = 1
    userlike = 1
    payload = {'success':True}
    if request.user.is_authenticated:
        if request.method == 'POST':
            postInst = getpostCount(PostCount)
            userInst = getpostby(PostLikeBy,request.user.id)
            if not userInst:
                obj = savepost(PostLikeBy,request,like=0,dlike=1,savetype='save')
                obj.save()
            else:
                if userInst.like == 1:
                    userlike = -1     
                else:
                    userlike = 0

                if userInst.dislike == 0:                  
                    obj = savepost(PostLikeBy,request,instance=userInst.id,like=0,dlike=1,savetype='update') 
                    
                else:
                    obj = savepost(PostLikeBy,request,instance=userInst.id,like=0,dlike=0,savetype='update')                      
                    payload = {'success':False}     
                    totallike = -1    

                obj.save() 
            if postInst:
                user_like_or_dlike = Postinstance(postInst,ulike=userlike, udlike = totallike)
                payload['likes'] = user_like_or_dlike[0]
                payload['dislikes'] = user_like_or_dlike[1]
        return JsonResponse(payload)
    return redirect('/login') 
     
def getpostCount(model):
   return model.objects.get(id=1)

def getpostby(model,id):
    instance = None
    try :
        instance = model.objects.get(user = id)
    except:
        pass

    return instance 

def likeView(request): 
    userInst = None
    totallike = 1
    userlike = 1
    payload = {'success':True}
    if request.user.is_authenticated:
        if request.method == 'POST':
            postInst = getpostCount(PostCount)
            userInst = getpostby(PostLikeBy,request.user.id)
            if not userInst:
                obj = savepost(PostLikeBy,request,like=1,dlike=0,savetype='save')
                obj.save()
            else:
                if userInst.dislike == 1:
                    userlike = -1
                else:
                    userlike = 0

                if userInst.like == 0:
                    obj = savepost(PostLikeBy,request,instance=userInst.id,like=1,dlike=0,savetype='update')  
                else:
                    obj = savepost(PostLikeBy,request,instance=userInst.id,like=0,dlike=0,savetype='update')                     
                    totallike = -1
                    payload = {'success':False}                    
                obj.save()     
            if postInst:
                user_like_or_dlike = Postinstance(postInst,ulike=totallike,udlike=userlike)                
                payload['likes'] = user_like_or_dlike[0]
                payload['dislikes'] = user_like_or_dlike[1]

        return JsonResponse(payload)
    return redirect('/login') 
  
def savepost(model,request = None,**kwarg):
    obj = None
    userid = kwarg.get('instance',None)
    userLike = kwarg.get('like',None)
    userDlike = kwarg.get('dlike',None)
    savetype = kwarg.get('savetype',None)

    if savetype == 'save':
        obj = model(user=request.user,like=userLike,dislike=userDlike)
    elif savetype == 'update':
        obj =  model(id = userid, user=request.user,like=userLike,dislike=userDlike)
    else:
        obj =  model(id = userid,like=userLike,dislike=userDlike)
    return obj

def Postinstance(instance,ulike =0,udlike=0):
    id = instance.id
    likes = instance.like + ulike
    dlikes = instance.dislike + udlike
    obj = savepost(PostCount,instance=id,like=likes,dlike=dlikes)  
    obj.save()     
    return [likes,dlikes]

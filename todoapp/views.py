from django.shortcuts import render,redirect

from .forms import SignupForm,UserProfileForm

from .models import UserProfile,ToDoList,ToDoPoints,City,Connects

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from .utils import sendOTP,reCaptcha,verifyEmail

from django.http import HttpResponse

import json

from django.core import serializers

# Create your views here.
def index_view(request):
	return render(request, 'todoapp/index.html')

def signup_view(request):
	if request.method=='POST':
		verified=reCaptcha(request)

		if verified:						
			form=SignupForm(request.POST)
			user=form.save()
			user.set_password(user.password)
			user.is_active=0
			user.save()
			
			#verifyEmail(request,user)			

			return render(request, 'todoapp/aftersignup.html')
		else:
			return redirect('/todoapp/signup')
		
	else:
		form=SignupForm()
		return render(request, 'todoapp/signup.html', {'form':form})


def account_activation_view(request):
	uid=request.GET.get('id')
	request.session['uid'] = uid

	uname=request.GET.get('uname')
	request.session['uname'] = uname
	
	actcode=request.GET.get('act_code')
	activation_code=str(request.session.get('activation_code'))
	
	try:
		user=User.objects.get(id=uid)
		if actcode==activation_code:
			user.is_active=1
			user.save()

			return redirect('/todoapp/profile')
	except:
		return render(request, 'todoapp/error.html')

	
def profile_view(request):
	if request.method=='POST':
		profpic=request.FILES.get('profpic')
		mobile=request.POST.get('mobile')
		ctid=request.POST.get('city')
		uid=request.session['uid']
		
		uf=UserProfile(user_id=uid,city_id=ctid,mobile=mobile,profpic=profpic)
		uf.save()

		#form=UserProfileForm(request.POST)
		return redirect('/accounts/login')
	else:
		form=UserProfileForm()
		return render(request, 'todoapp/profile.html', {'form':form})

@login_required
def show_todos_view(request):
	uid=request.session['_auth_user_id']
	userprof=UserProfile.objects.get(user_id=uid)

	alltodos=ToDoList.objects.filter(userprof_id=userprof.id)

	if request.method=='POST':
		title=request.POST.get('title')		
		todotypeid=request.POST.get('urselection')
		todolist=ToDoList(title=title,userprof_id=userprof.id,todotype_id=todotypeid)
		todolist.save()		
		return redirect('/todoapp/showtodos')
	else:		
		return render(request, 'todoapp/todolist.html', {'todos':alltodos})

@login_required
def dashboard_view(request):
	request.session['login']=True
	return render(request, 'todoapp/dashboard.html')

def sendotp_view(request):
	mobnum=request.GET.get('mobile')

	#sendOTP(mobnum,request)

	return HttpResponse('done')

def checkotp_view(request):
	resp = 'false';
	
	userotp=request.GET.get('otp')
	serverotp=request.session['otp']
	
	'''
	if(userotp==serverotp):
		resp = 'true'
	'''
	###
	resp = 'true'

	return HttpResponse(resp)


def change_title_view(request):
	title=request.GET.get('title')
	todoid=request.GET.get('todoid')

	todoobj=ToDoList.objects.get(id=todoid)
	todoobj.title=title
	todoobj.save()

	return HttpResponse("done")

#Old
'''
def delete_textnote_view(request):
	todoid=request.GET.get('todoid')
	todorec=ToDoList.objects.get(id=todoid)
	todorec.delete()

	return HttpResponse('done')
'''

#New
def delete_todo_view(request):
	todoid=request.GET.get('todoid')
	todoobj=ToDoList.objects.get(id=todoid)
	todoobj.delete()

	return HttpResponse('done')

def save_textnote_view(request):
	todoid=request.GET.get('todoid')
	textnote=request.GET.get('textnote')
	todorec=ToDoList.objects.get(id=todoid)
	todorec.textnote=textnote
	todorec.save()

	return HttpResponse('done')




@login_required
def save_checklist_view(request):
	todopoints=request.GET.getlist('point')
	actives=request.GET.getlist('active')
	todoid=request.GET.get('todoid')

	allpoints=ToDoPoints.objects.filter(todolistid_id=todoid)
	for point in allpoints:
		point.delete()
	
	i=0
	for todop in todopoints:
		active=eval(actives[i].capitalize())
		i+=1
		status_id = 1 if active else 2
		print(status_id)
		todopoint=ToDoPoints(todopoint=todop,todolistid_id=todoid,status_id=status_id)
		todopoint.save()

	return HttpResponse('done')

@login_required
def all_points_view(request):
	resp='norecords'
	
	todoid=request.GET.get('todoid')

	uid=request.session['_auth_user_id']
	userprof=UserProfile.objects.get(user_id=uid)

	recs=ToDoList.objects.filter(userprof_id=userprof.id,id=todoid)
	
	if len(recs)==1:
		todopoints=ToDoPoints.objects.filter(todolistid_id=todoid)	
		
		if len(todopoints)!=0:	
			ser=serializers.serialize('json',todopoints)
			points=json.loads(ser)
			resp=json.dumps(points)
	else:
		resp='wrong'

	return HttpResponse(resp)

def set_point_done_view(request):
	todopointid=request.GET.get('todopointid')

	todopoint=ToDoPoints.objects.get(id=todopointid)
	todopoint.status_id=2
	todopoint.save()

	return HttpResponse('done')


def set_point_active_view(request):
	todopointid=request.GET.get('todopointid')

	todopoint=ToDoPoints.objects.get(id=todopointid)
	todopoint.status_id=1
	todopoint.save()

	return HttpResponse('done')


def show_connects_view(request):
	return render(request, 'todoapp/connects.html')

def search_user_view(request):	
	searchkey=request.GET.get('searchkey')
	
	users=User.objects.filter(username__contains=searchkey)
	
	ser=serializers.serialize('json',users)
	usrs=json.loads(ser)	

	return HttpResponse(json.dumps(usrs))
	

def user_detail_view(request):
	userid=request.GET.get('userid')
	uid=request.session['_auth_user_id']
	
	user=User.objects.get(id=userid)
	userprof=UserProfile.objects.get(user_id=userid)
	city=City.objects.get(id=userprof.city_id)
	cons=Connects.objects.filter(from_user_id=uid,to_user_id=userid)|Connects.objects.filter(from_user_id=userid,to_user_id=uid)
	
	print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
	print(cons) 
	print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
	lst=[user,userprof,city]
	if len(cons)!=0:
		lst.append(cons.first())

	
	ser=serializers.serialize('json',lst)
	
	usr=json.loads(ser)

	return HttpResponse(json.dumps(usr))	
	

def start_connection_view(request):
	touserid=request.GET.get('touserid')
	fromuid=request.session['_auth_user_id']

	con=Connects(from_user_id=fromuid,to_user_id=touserid)
	con.save()

	return HttpResponse('done')

def change_connection_status_view(request):
	conid=request.GET.get('conid')
	stid=int(request.GET.get('stid'))

	if stid==0:
		con=Connects.objects.get(id=conid)
		con.delete()
	else:
		con=Connects.objects.get(id=conid)
		con.status_id=stid
		con.save()

	return HttpResponse('done')
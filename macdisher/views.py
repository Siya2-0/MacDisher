from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage
from django.views import View
from config import permissions
from django.contrib.auth.models import User
from macdisher.serializers import MacSerializer

from .models import Mac, Allocation, Device
from django.db import connection
from django import forms
from .forms import   DropDownFilterForm, ReserveMacForm
from .function import FindLargeFreeMacAddress, ReturnPendingMACPerUser
import csv
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf  import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.pagination import PageNumberPagination




#parameter : request
#this view handles home page view
def macdisher_index(request):

    return render(request, 'home.html')

#parameter: request
#this view handles the  search functionality ( mac : device : allocation)
@login_required
def macdisher_filter(request):#change name to filter
    Paginate1= Paginator(ReturnPendingMACPerUser(request.user.username), 5)
    CountPending=ReturnPendingMACPerUser(request.user.username).count()
    Pending=Paginate1.page(1)

    if(request.method=="POST"):


        results=Mac.objects.all()
        form=DropDownFilterForm(request.POST)


        if form.is_valid():
            MacCondition=form.cleaned_data['MacInput']
            AllocationCondition=form.cleaned_data['AllocationInput']
            DeviceCondition=form.cleaned_data['DeviceInput']



            if MacCondition != "":
                results=results.filter(mac=MacCondition)
            if AllocationCondition.__str__() != "":
                results=results.filter(allocation=AllocationCondition)
            if DeviceCondition.__str__() !="" :
                results=results.filter(device=DeviceCondition)
            if MacCondition == "" and  AllocationCondition.__str__() == ""  and DeviceCondition.__str__() =="": #error condition form input not given
                results=results.filter(mac="")
                ErrorMessgeList=['All Input Field Not Filled']
                return  render (request ,'macdisher/index.html',{'results': results,'form':DropDownFilterForm(), 'number':results.count(), 'messages':ErrorMessgeList, 'Pending':Pending, 'CountPending': CountPending})



            ParameterList=[MacCondition, AllocationCondition.__str__(), DeviceCondition.__str__()]
            CommaSeparatedList=""
            for item in ParameterList:
                CommaSeparatedList = CommaSeparatedList +str(item) +","

            if results.count()==0:
                ErrorMessgeList=['Mac Address not found']
                if MacCondition != "":
                    ErrorMessgeList[0]+=": MAC:"+MacCondition+"  "
                if AllocationCondition.__str__() != "":
                    ErrorMessgeList[0]+=": ALLOCATION: "+AllocationCondition.__str__() +"  "
                if DeviceCondition.__str__() !="" :
                    ErrorMessgeList[0]+=": DEVICE: "+DeviceCondition.__str__() +"  "
                return render (request ,'macdisher/index.html',{'results': results,'form':DropDownFilterForm(), 'number':results.count(),'messages_Nothing_Found':ErrorMessgeList , 'Pending':Pending , 'CountPending': CountPending})
            else:
                Paginate= Paginator(results, 10)
                PageOne=Paginate.page(1)
                return render (request, 'macdisher/index.html', {"results":PageOne, 'form':DropDownFilterForm(), 'number': results.count(), 'Paralist': CommaSeparatedList , 'Pending':Pending, 'CountPending': CountPending})



    #GET request
    form=DropDownFilterForm()
    return render(request ,'macdisher/index.html',{"form": form, 'Pending':Pending , 'CountPending': CountPending})


#parameter: request
#this view  reserves mac address (count : device : metasring)
@login_required
def macdisher_reserve(request):

    if request.method =="POST" and request.user.is_authenticated:
        form=ReserveMacForm(request.POST)
        if form.is_valid():
            count=form.cleaned_data['Count']
            deviceObject=form.cleaned_data['Device']
            metaData=form.cleaned_data['MetaData']

            PendingCount=0 #counts addrress replaced by pending records
            ReservedAddress=[]
            PendingRequests=Mac.objects.all().filter(allocation="PENDING",user=request.user.username )#update to case insentitve
            for pending in PendingRequests :
                if PendingCount<count:
                    pending.device=deviceObject.__str__()
                    pending.metastring=metaData
                    pending.allocation="PENDING"
                    pending.save()
                    PendingCount+=1
                    ReservedAddress.append(pending)
                else:
                    break


            RemainingRequestCount=count-PendingCount
            message=""
            for EachReqest in range(0, RemainingRequestCount):
                address=FindLargeFreeMacAddress()#fix assumption that mac address will assigned sequentially
                if address is None:
                    ErrorList=["Address in Range maclimit |maclimits.start=34298FD00000|maclimits.end=34298FDFFFFF|"]
                    if len(ReservedAddress) == 0:
                        ErrorList.append("Zero Mac Address Reserved ")
                        return  render(request, 'macdisher/reserve.html', {"form":form, "ReservedAddress":ReservedAddress, 'messages':ErrorList})
                    else:
                        Paginate= Paginator(ReservedAddress, 10)
                        PageOne=Paginate.page(1)
                        ErrorList.append(str(len(ReservedAddress))+" Mac Address Reserved ")
                        return render (request, 'macdisher/reserve.html', {"form":form, "ReservedAddress":PageOne, 'counts': len(ReservedAddress), 'messages':ErrorList})


                else:
                    MacRecord= Mac(allocation='PENDING', device=deviceObject.__str__(), mac=address[2:], metastring=metaData, time=datetime.now(), user=request.user.username)
                    MacRecord.save()
                    ReservedAddress.append(MacRecord)
                    PendingCount+=1


            if len(ReservedAddress) == 0 or count<=0:
                ErrorList=["count value invalid"]
                return  render(request, 'macdisher/reserve.html', {"form":form, "ReservedAddress":ReservedAddress, 'messages':ErrorList})
            else:
                Paginate= Paginator(ReservedAddress, 10)
                PageOne=Paginate.page(1)
                return render (request, 'macdisher/reserve.html', {"form":form, "ReservedAddress":PageOne, 'counts': len(ReservedAddress)})
        #assumption successful  full allocation




    form= ReserveMacForm()
    Paginate1 = Paginator(ReturnPendingMACPerUser(request.user.username), 10)
    CountPending = ReturnPendingMACPerUser(request.user.username).count()
    Pending = Paginate1.page(1)
    return render(request, 'macdisher/reserve.html', {"form": form, "ReservedAddress":Pending, 'counts': CountPending})



#parameter : request
#view handles assignment of mac address, From Pending to Assigned

@csrf_exempt
@login_required
def macdisher_assign(request):

    if request.method=="POST":
        MacToBeAssigned=request.POST.getlist("CheckBox")
        for EachMac in MacToBeAssigned:
            try:
                update=Mac.objects.get(id=EachMac)
                update.allocation="ASSIGNED"
                update.save()
            except ObjectDoesNotExist:
                  print("No matching ID found.", EachMac)



    return redirect("/mcdisher/reserve/")

#parameter request  , pagenumber : int, count : int
#this view hanges pagination of the request mac address( paging between pages)
@login_required
def macdisher_pagniate_GET_MAC(request, pagenumber, count):

    if request.user.is_authenticated:
        results=Mac.objects.all().filter(allocation="PENDING",user=request.user.username)[0:count]

        Paginate= Paginator(results, 10)

        if(results.count() != 0):
            try:
                PageOne=Paginate.page(pagenumber)
                return render (request, 'macdisher/reserve.html', {"ReservedAddress":PageOne, 'form':ReserveMacForm(), 'counts': count})
            except EmptyPage:
                PageOne=Paginate.page(1)
                render (request, 'macdisher/reserve.html', {"ReservedAddress":PageOne, 'form':ReserveMacForm(), 'counts': count})



    return render(request, 'macdisher/reserve.html', {'form':ReserveMacForm()})

#parameters: request,  pagenumber: int , list :string
#this view handles pagination between the search result
@login_required
def macdisher_paginate(request, pagenumber, list):
    Paginate1 = Paginator(ReturnPendingMACPerUser(request.user.username), 5)
    CountPending = ReturnPendingMACPerUser(request.user.username).count()
    Pending = Paginate1.page(1)

    results=Mac.objects.all()
    ParameterList=list.split(",")

    if(len(ParameterList) != 4):
        return redirect("/mcdisher/search/")


    if ParameterList[0] != "":
        results=results.filter(mac=ParameterList[0])
    if ParameterList[1] != "":
        results=results.filter(allocation=ParameterList[1])
    if ParameterList[2] !="" :
        results=results.filter(device=ParameterList[2])
    if ParameterList[0] == "" and  ParameterList[1] == ""  and ParameterList[2]=="":
        results=results.filter(mac="")




    if(results.count() != 0):
        Paginate= Paginator(results, 10)
        try:
            PageOne=Paginate.page(pagenumber)
            return render (request, 'macdisher/index.html', {"results":PageOne, 'form':DropDownFilterForm(), 'number': results.count(), 'Paralist': list, 'Pending':Pending , 'CountPending': CountPending})
        except EmptyPage:
            PageOne=Paginate.page(1)
            render (request, 'macdisher/index.html', {"results":PageOne, 'form':DropDownFilterForm(), 'number': results.count(), 'Paralist': list, 'Pending':Pending , 'CountPending': CountPending})

    return render (request, 'macdisher/index.html', {"results":results, 'form':DropDownFilterForm(), 'number': results.count(), 'Paralist': list, 'Pending':Pending , 'CountPending': CountPending})

#paramter: reqeuest, pagenumber: int
#this view handles the paginaion  of pending mac address in the search page
@login_required
def Pending_Pagination(request, pagenumber):
    pending=ReturnPendingMACPerUser(request.user.username)
    Paginate= Paginator(pending, 5)
    try:
        PageOne=Paginate.page(pagenumber)
        return render (request, 'macdisher/index.html', {"Pending":PageOne, 'form':DropDownFilterForm(), 'CountPending': pending.count()})
    except EmptyPage:
        PageOne=Paginate.page(1)
        render (request, 'macdisher/index.html', {"Pending":PageOne, 'form':DropDownFilterForm(), 'CountPending': pending.count()})



#paramter: request, list:string
#this view handles the exportation of results into a CSV
@login_required
def macdisher_export_CSV(request, list):
    results=Mac.objects.all()
    ParameterList=list.split(",")

    if(len(ParameterList) != 4):
        return redirect("/mcdisher/search/")

    if ParameterList[0] != "":
        results=results.filter(mac=ParameterList[0])
    if ParameterList[1] != "":
        results=results.filter(allocation=ParameterList[1])
    if ParameterList[2] !="" :
        results=results.filter(device=ParameterList[2])
    if ParameterList[0] == "" and  ParameterList[1] == ""  and ParameterList[2]=="":
        results=results.filter(mac="")

    filename='mac_address.csv'
    response=HttpResponse(content_type='text/csv')
    response['Content-Dispostion']='attachment; filename={}'.format(filename)

    writer=csv.writer(response)

    writer.writerow(['ID', 'ALLOCATION', 'DEVICE', 'MAC', 'METASTRING', 'TIME', 'USER'])

    for record in results:
        writer.writerow([record.id, record.allocation, record.device, record.mac, record.metastring, record.time, record.user ] )

    return response


#API 
#parameter request
#This view reserves mac address (count : device: metastring)
@api_view(['POST', 'GET'])
def Post_Reserve_Request(request):
    pagination_class = PageNumberPagination
    if getattr(settings, "username", None) is None or getattr(settings, "username", None)=="":
        return Response({'status': 'Not logged In'}, status=401)

    if request.method=='GET':
        return Response({"count":"Enter Count", "device": "Enter Device", "metastring": "Enter metastring" }, status=200)


    if request.method=='POST'  :
        if 'device' not in request.data:
            return Response({"Error":"device not given"}, status=403)


        count=1#default
        meta="None"#default
        if('count' in request.data):
            count =int(request.data['count'])

        if 'metastring' in request.data and request.data['metastring'] != "":
            meta=request.data['metastring']


        if(Mac.objects.filter(device=request.data['device']).count()==0):
           #DECLARE  404 ERROR
            return Response({"InputDevice": "Does not exist", 'device':request.data['device']}, status=404)

        PendingCount=0 #counts addrress replaced by pending records
        ReservedAddress=[]
        PendingRequests=Mac.objects.all().filter(allocation="PENDING",user=getattr(settings, "username", None) )#update to case insentitve
        for pending in PendingRequests :
            if PendingCount< count:
                pending.device=request.data['device']
                pending.metastring=meta
                pending.allocation="PENDING"
                pending.save()
                PendingCount+=1
                ReservedAddress.append(pending)
            else:
                break

        RemainingRequestCount=count-PendingCount
        message=""
        for EachReqest in range(0, RemainingRequestCount):
            address=FindLargeFreeMacAddress()
            if address is None:

                if len(ReservedAddress) == 0:
                    #declare 403 error zero allocated address
                    return Response({"MacAddress" :"used up", "description" :"Address space  in range used up"}, status=403)
                else:
                    #declare a 201 error
                    pagination = PageNumberPagination()
                    page = pagination.paginate_queryset(ReservedAddress, request)
                    serializer=MacSerializer(page,  many=True)
                    return Response(serializer, status=201)



            else:
                MacRecord= Mac(allocation='PENDING', device=request.data['device'], mac=address[2:], metastring=meta, time=datetime.now(), user=getattr(settings, "username", None))
                MacRecord.save()
                ReservedAddress.append(MacRecord)
                PendingCount+=1


        if len(ReservedAddress) == 0:
            #declare a 200 error
            return Response({"mac":"no mac reserved"}, status=200)

        else:
            #declare a 200 reponse
            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(ReservedAddress, request)
            serializer=MacSerializer(page, many=True)
            return Response(serializer.data, status=200)




    #declare a 401 error
    return Response({'login': 'invalid'}, status=401)




#API 
#parameter request
#This view search for mac address (allocation : device: user: count)
@api_view(['POST', 'GET'])
def  POST_AllMac(request):
    pagination_class = PageNumberPagination
    if getattr(settings, "username", None) is  None or getattr(settings, "username", None)=="":
        return Response({'status': 'Not logged In'}, status=401)

    if request.method=='GET':
        return Response({"allocation":"Enter allocation", "device": "Enter Device", "user": "Enter User Name", "count": "Enter Count" }, status=200)

    if request.method=='POST':
        OutputData=Mac.objects.all()

        if('device'  in request.data  and Mac.objects.filter(device=request.data['device']).count()==0  ):
            return Response({'Input': "Invalid", "device":request.data['device']}, status=404)
        elif 'device'  in request.data:
            OutputData=OutputData.filter(device=request.data['device'])

        if 'allocation' in request.data  and Mac.objects.filter(allocation=request.data['allocation']).count()==0 :
            return Response({'Input': "Invalid", "allocation":request.data['allocation']}, status=404)

        elif 'allocation' in request.data:
            OutputData=OutputData.filter(allocation=request.data['allocation'])

        if 'user' in request.data:
            OutputData=OutputData.filter(user=request.data['user'])


        if 'device' not in request.data  and  'allocation' not in request.data and  'user' not in request.data and 'count' not in request.data:
            OutputData=Mac.objects.none()

        pagination = PageNumberPagination()
        # paginated_queryset = paginator.paginate_queryset(queryset, request)
        if('count' in request.data  and int(request.data['count'])<0):
            #404 erro
            return Response( {'Input': "Invalid", "count": request.data['count']}, status=404)
        elif 'count' in request.data:
            pagination.page_size=int(request.data['count'])


        page = pagination.paginate_queryset(OutputData, request)
        serializer=MacSerializer(page, many=True)
        return Response(serializer.data, status=200)

    #error 401
    return Response({'login': 'invalid'}, status=401)




#API 
#parameter request
#This view changes mac's allocattion from Pending to Assignment
@api_view(['POST', 'GET'])
def POST_AssignMac(request):
    if getattr(settings, "username", None) is  None or getattr(settings, "username", None)=="":
        return Response({'status': 'Not logged In'}, status=401)
    if request.method=='GET':
        return Response({"macs":['string']}, status=200)

    if request.method=='POST':
        if 'macs' not in request.data:
            return Response({'macs': 'mac not given'}, status=200)
        else:
            for each in request.data['macs']:
                try:
                    MacAddress=Mac.objects.get(mac=each)

                    if MacAddress is None:
                        print("Mac does not exit")
                    elif MacAddress.allocation=="ASSIGNED":
                        return Response({'mac': each, 'Error':"already assigned"}, status=403)
                    else:
                        MacAddress.allocation="ASSIGNED"
                        MacAddress.save()
                except ObjectDoesNotExist:
                        print("No matching object found. ",each)

            return Response({}, status=200)

    #error 401
    return Response({'login': 'invalid'}, status=401)

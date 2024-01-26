from .models import Mac
from django.conf import settings
from django.contrib.sites.models import Site

def FindLargeFreeMacAddress():
    MacRecords=Mac.objects.all()
    MacRecords_Range=[]
    for MR in MacRecords:
        if hex(int(MR.mac, 16))>= hex(int("34298FD00000", 16))  and hex(int(MR.mac, 16))<=hex(int("34298FDFFFFF", 16)):
            MacRecords_Range.append(MR)


    if(len(MacRecords_Range)==0):
        return hex(int("34298FD00000",16))
    
    

    MacRecords_Range.sort(reverse=True, key=MacAddressValue)
    if hex(int(MacRecords_Range[0].mac, 16) +1) > hex(int("34298FDFFFFF",16)):
        return SequentialSearchOfAvaiableMacAddress()
    
    
    return (hex( int(MacRecords_Range[0].mac, 16)  + 1 ) )
   # return len(MacRecords_Range)


def MacAddressValue(MacRecord):

    return hex(int(MacRecord.mac, 16))  


def SequentialSearchOfAvaiableMacAddress():
    
    current=(hex( int("34298FD00000", 16) ) )
    while current <= hex(int("34298FDFFFFF", 16)):

        if Mac.objects.filter(mac=str(current)[2:]):
            current= current+hex(1)
        else:#open space
            return current

    return None




def ReturnPendingMACPerUser(username: str): # ASSUMPTION: Valid User Name
   macs=Mac.objects.all()
   macs=macs.filter(user=username, allocation="PENDING")
   return macs
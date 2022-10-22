import csv
import math
import os
import datetime

rooms=[
          ["I","101","SD","V",1200],
          ["I","102","SD","V",1200],
          ["I","103","D","V",1500],
          ["I","104","SD","V",1200],
          ["I","105","SDX","V",2000],
          ["I","106","SD","V",1200],
          ["II","201","SDX","V",2000],
          ["II","202","SD","V",1200],
          ["II","203","D","V",1500],
          ["II","204","D","V",1500],
          ["II","205","SDX","V",2000],
          ["II","206","SD","V",1200],
          ["III","301","SDX","V",2000],
          ["III","302","HDX","V",4000],
          ["III","303","SDX","V",2000],
          ["III","304","D","V",1500],
          ["III","305","SDX","V",2000]
    ]          
 
def ShowMenu():
          print("\n\n\n\t\t############ HOTEL R.P ###############")
          print("\n\t\t\t 1. All ROOM STATUS ")
          print("\n\t\t\t 2. CHECK-IN ")
          print("\n\t\t\t 3. CHECK-OUT ")
          print("\n\t\t\t 4. OTHER EXPENSES ")
          print("\n\t\t\t 5. ROOM ENQUIRY ")
          print("\n\t\t\t 6. CONTACT DETAIL")
          print("\n\t\t\t 0. LOG OUT ")
          print("\t\t#########################################")

def ShowAllRoomStatus():
    with open('rooms.csv', mode='r') as csvfile:
        myreader = csv.reader(csvfile,delimiter='|')
        print("="*75)
        print("%10s"%"FLOOR","%15s"%"ROOM NUMBER","%20s"%"ROOM TYPE","%15s"%"ROOM STATUS",'%10s'%'RATE')
        print("="*75)
        for row in myreader:
            if row[2]=="D":
                    rtype="DELUXE"
            elif row[2]=="SD":
                    rtype="SEMI-DELUXE"
            elif row[2]=="SDX":
                    rtype="SUPER DELUXE"
            elif row[2]=="HDX":
                    rtype="EXECUTIVE SUITE"
            if row[3]=="V":
                    status="VACANT"
            else:
                    status ="OCCUPIED"
            print("%10s"%row[0],"%15s"%row[1],"%20s"%rtype,"%15s"%status,'%10s'%row[4])
        print("="*75)
    input('Press any key...')

def CheckRoomVacant(roomno):
    with open('rooms.csv',mode='r') as csvfile:
        myreader = csv.reader(csvfile,delimiter='|')
        found=False
        for row in myreader:
            if len(row)>0:
                if str(row[1])==str(roomno):
                    found=True
                    return row[3],row[4]
        if not found:
            return 'INVALID'         
    input('Press any key...')         

def CheckIn():
    print('\n\n\t\t################# NEW VISITOR ARRIVAL #######################')
    dt = datetime.datetime.now()
    today = str(dt.day)+'/'+str(dt.month)+'/'+str(dt.year)+' '+str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second)
    print('\n\t\t\t\t\t\t\t Today is :'+today)
    #print('\n\t\t Visitor Number :',Visitor_Number)
    name = input('\t\t Enter Visitor Name :')
    ID = input('\t\t Enter What Photo ID number :')
    age = int(input('\t\t Enter Age :'))
    gender = input('\t\t Choose gender (Press 1 for male and any other key for female:')
    coming_from = input('\t\t Enter the Place from where person is coming :')
    purpose = input('\t\t Enter purpose of Visit :')
    mobile = input('\t\t Enter Mobile Number :')
    c='go'
    roomno=0
    while c=='go':
        roomno = int(input('\t\t Enter Room Number :'))
        status = CheckRoomVacant(roomno)
        if status[0]=='INVALID':
            print('Enter Valid room number :')
        elif status[0]=='V':
            c='OK'
        else:
            print('Room Number not Vacant')
    print('\t\t Check in Date and Time :',today)
    print('\t\t Room Rent @'+str(status[1])+' Day')
    print('\t\t Advance To Pay :'+str(status[1]))
    ans = input('\n\t\t Confirm?(y)')
    if ans.lower()=='y':
        visitors=[name,ID,age,gender,coming_from,purpose,roomno,today,status[1],mobile]
        with open('Visitor.csv','a') as vfile:
            mywriter = csv.writer(vfile,delimiter='|',lineterminator='\n')
            mywriter.writerow(visitors)
        print('\n\t\t Checked In Successfully!')
        room=[]
        with open('rooms.csv','r') as rcsv:
            myreader = csv.reader(rcsv,delimiter='|')
            for row in myreader:
                if len(row)>0:
                    room.append(row)
                    #print(row)

        with open('rooms.csv','w') as rcsv:
            mywriter = csv.writer(rcsv,delimiter='|',lineterminator='\n')
            for i in range(len(list(room))):
                if room[i][1]==str(roomno):
                            room[i][3]='O'
                #print(room[i])
                mywriter.writerow(room[i])

def OtherExpense():
    print("="*30," OTHER EXPENSE SCREEN ", "="*30)
    visitors=[]
    with open('Visitor.csv','r') as csvroom:
        myreader = csv.reader(csvroom,delimiter='|')
        for row in myreader:
                    visitors.append(row)
    rno = input('\n\t\t ENTER ROOM NO :')
    found=False
    for rs in visitors:
        if rs[6]==rno:
            food = int(input('Enter Food Expense (0 if no expense):'))
            laundry = int(input('Enter Laundry Expense (0 if no expense) :'))
            misc = int(input('Enter any other expense (0 if no expense) :'))
            with open('expense.csv','a') as expcsv:
                mywriter = csv.writer(expcsv,delimiter='|',lineterminator='\n')
                today = datetime.datetime.now()
                today = str(today.day)+'/'+str(today.month)+'/'+str(today.year)
                exp = [rno,food,laundry,misc,today]
                mywriter.writerow(exp)
            found=True
    if not found:
        print("\n### SORRY ROOM NUMBER NOT OCCUPIED ###")

def CheckOut():
    print('\n\n')
    print('='*30,' CHECK OUT SCREEN ' , '='*30)
    roomstatus=[]
    with open('rooms.csv','r') as csvroom:
        myreader = csv.reader(csvroom, delimiter='|')
        for row in myreader:
            roomstatus.append(row)
    rno = input('\n\t\t ENTER ROOM NO :')
    found=False
    vis=[]
    fexp=0
    lexp=0
    mexp=0
    total=0
    oexp=0
    for rs in roomstatus:                 
        if rs[1]==rno and rs[3]=='O':
            rs[3] = 'V'
            total=total + int(rs[4])
            print('Checking....')
            visstatus=[]
            with open('Visitor.csv','r') as vcsv:
                myreader = csv.reader(vcsv,delimiter='|')
                for row in myreader:
                    if rno == row[6]:
                        vis = row
                        print("In")
                    else:                      
                        visstatus.append(row)
            
            if (os.path.exists('expense.csv')):
                expstatus=[]
                with open('expense.csv','r') as ecsv:
                    myreader = csv.reader(ecsv,delimiter='|')
                    for row in myreader:
                        if row[0]==rno:
                            fexp = fexp + int(row[1])
                            lexp = lexp + int(row[2])
                            mexp = mexp + int(row[3])
                        else:                      
                            expstatus.append(row)
                oexp = fexp + lexp + mexp
            found = True
    if not found:
        print('## ROOM NOT BOOKED ##')
    else:
        today = datetime.datetime.now()
        today = str(today.day)+'/'+str(today.month)+'/'+str(today.year)+' '+str(today.hour)+':'+str(today.minute)+':'+str(today.second)
        print('\n\n')
        print('='*30,'CHECK OUT (BILL)','='*30)
        print('\t\t CHECK IN DATE : ',vis[7])
        print('\t\t CHECK OUT DATE :',today)
        print('-'*75)
        #print('\t\t Visitor Number : ',vis[0])
        print('\t\t Visitor Name   : ',vis[0])
        print('\t\t Visitor Age    : ',vis[2])
        g=''
        if vis[4]=='1':
            g='Male'
        else:
            g='Female'
                    
        print('\t\t Visitor Gender : ',g)     
        print('\t\t Coming From     : ',vis[4])
        print('\t\t Purpose of Visit: ',vis[5])
        print('-'*75)

        d1 = datetime.datetime.strptime(vis[7],"%d/%m/%Y %H:%M:%S")
        d2 = datetime.datetime.strptime(today,"%d/%m/%Y %H:%M:%S")
        d3 = d2-d1
        day=0
        if d3.days<=1:
                    day=1
        else:
                    day = math.ceil(d3.days)
        print('\n\t\t Total days          :',day)
        print('\t\t Room Rent @'+str(total)+'/Day :Rs.',total*day)
        print('\t\t Food Expense        :Rs.',fexp)
        print('\t\t Laundry Expense     :Rs.',lexp)
        print('\t\t Misc. Expense       :Rs.',mexp)
        print('-'*75)
        print('\t\t\t GRAND TOTAL : Rs.',(total+oexp))

        #Update rooms.csv file
        with open('rooms.csv',mode='w') as csvfile:
            mywriter = csv.writer(csvfile,delimiter='|', lineterminator='\n')
            for r in roomstatus:
                mywriter.writerow(r) 

        with open('Visitor.csv',mode='w') as csvfile:
            mywriter = csv.writer(csvfile,delimiter='|', lineterminator='\n')
            for r in visstatus:
                mywriter.writerow(r)

        with open('expense.csv',mode='w') as csvfile:
            mywriter = csv.writer(csvfile,delimiter='|', lineterminator='\n')
            for r in expstatus:
                mywriter.writerow(r)
                    
def RoomEnquiry():
    print('\n\n')
    print('='*30,' VISITOR ENQUIRY SCREEN ' , '='*30)
    vn = input("\n\t\t ENTER VISITOR NAME : ")
    fs = "%-15s %6s %10s %15s %15s %8s %-20s"
    print(fs % ("VISITOR NAME","AGE","GENDER","COMING FROM","PURPOSE","ROOMNO","CHECKIN DATE"))
    print("="*110)
    found=False
    gender=''
    with open('Visitor.csv','r') as vcsv:
        myreader = csv.reader(vcsv,delimiter='|')
        for row in myreader:
            if row[0].lower()==vn.lower():
                if row[3]=='1':
                    gender='Male'
                else:
                    gender='Female'
                print(fs%(row[0],row[2],gender,row[4],row[5],row[6],row[7]))
                found=True
    print("="*110)
    if not found:
            print("\n\t\t\t VISITOR NAME NOT FOUND ")

def Contact():
          print("\n\n============================== CONTACT INFORMATION ==============================")
          print("\n\t\t Project Name : R.A.V HOTEL MANAGEMENT SYSTEM ")
          print("\n\t\t Developed By : RUMMAN PARVEZ ")
          print("\n\t\t E-Mail       : r.photelgwalior@gmail.com")
choice=7
while choice!=None:
    ShowMenu()
    if not os.path.exists('rooms.csv'):
        with open('rooms.csv',mode='w') as csvfile:
            mywriter = csv.writer(csvfile,delimiter='|',lineterminator='\n')
            for r in rooms:
                mywriter.writerow(r)        

    inputStr = input('\t\t\t ENTER YOUR CHOICE :')
    if inputStr and inputStr != '':
        choice = int(inputStr)
    else:
        choice = 7     
    if choice==1:
        ShowAllRoomStatus()
    elif choice==2:
        CheckIn()
    elif choice==3:
        CheckOut()
    elif choice==4:
        OtherExpense()
    elif choice==5:
        RoomEnquiry()
    elif choice==6:
        Contact()
    elif choice==0:
        choice = None
        print('\n\t\t\t THANK YOU!!!! FOR VISITING !!!!! VISIT AGAIN!!! ')
    else:
        print('\n\t\t\t == INVALID CHOICE == TRY AGAIN ==')

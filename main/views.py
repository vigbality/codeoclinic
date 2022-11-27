from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Users, Results, Images
from django.conf import settings
from cv2 import imread
import tensorflow as tf
from keras.models import load_model
import numpy as np
from hashlib import md5
import re
from cv2 import imread

def checkCardiomegaly(ridVal, phone, date, pData):
    imgObj = Images.objects.filter(rid=ridVal).first()
    im = imread(imgObj.image.path)
    new_model = load_model(settings.MEDIA_ROOT+'\\mask.h5', compile = False)
    image_grey = tf.image.rgb_to_grayscale(im)
    resize = tf.image.resize(image_grey, [512,512])
    yhat = new_model.predict(np.expand_dims(resize/255,0))
    output = np.reshape(yhat, [512,512])
    lowY, highY = 200, 0
    for r in range(512):
        for c in output[r,:]:
            if c== 1.0:
                highY = r
                break

    # for r in range(511,1,-1):
    #     for c in output[r,:]:
    #         if c == 1.0:
    #             lowY = r
    #             break

    lung = 0
    # print("cccccccc",lowY, highY)
    for r in range(lowY, highY):
        count = 0
        lengthL = 0
        for c in output[r,:]:
            if c == 1.0 and count ==0:
                count+=1
                lengthL+=1
            elif c == 1.0 and count == 1:
                lengthL+=1
            elif c != 1.0 and count == 1:
                count += 1
                lengthL+=1
            elif c != 1.0 and count == 2:
                lengthL+=1
            elif c == 1.0 and count ==2:
                count +=1
                lengthL+=1
            elif c == 1.0 and count ==3:
                lengthL+=1
            elif c != 1.0 and count ==3:
                break
        lung = max(lung,lengthL)
    # print(lung)
    val = (highY - lowY) // 2
    newL = lowY 
    newH = lowY + val 
    heart = 0
    for r in range(newL,newH):
        count =0    
        lengthH = 0
        for c in output[r,130:370]:
            if c == 1.0 and count ==0:
                count+=1
            elif c == 1.0 and count == 1:
                continue
            elif c != 1.0 and count == 1:
                count += 1
                lengthH+=1
            elif c != 1.0 and count == 2:
                lengthH+=1
            elif c == 1.0 and count ==2:
                break
        heart = max(heart,lengthH)

    ratio = round(heart/lung,4)
    if 0.35 < ratio < 0.75:
        result = 0
        if ratio > 0.50:
            result = 1
    else:
        imgObj = imread(imgObj.image.path)
        resize = tf.image.resize(imgObj, (512,512))
        new_model = load_model(settings.MEDIA_ROOT+'\\UIA_97_83.h5')
        yhat = new_model.predict(np.expand_dims(resize/255,0))
        result = 0
        if yhat > 0.5:
            result=1
        heart = lung = ratio = 'NA'
    if pData == []:
        Results(rid=ridVal, phone=phone, date=date,heart = heart,lung=lung,ratio=ratio, result=result, pPhone = "", pNotes = "", dPhone = "").save()
    else:
        Results(rid=ridVal, phone=phone, date=date,heart = heart,lung=lung,ratio=ratio, result=result, pPhone = pData['pphone'], pNotes = "", dPhone = "").save()
    return result







def getHashValue(phone, date):
    str2hash = phone+date
    result = md5(str2hash.encode())
    return result.hexdigest()


# def checkCardiomegaly(ridVal, phone, date, pData):
    imgObj = Images.objects.filter(rid=ridVal).first()
    imgObj = imread(imgObj.image.path)
    resize = tf.image.resize(imgObj, (512,512))
    new_model = load_model(settings.MEDIA_ROOT+'\\UIA_97_83.h5')
    yhat = new_model.predict(np.expand_dims(resize/255,0))
    result = 0
    if yhat > 0.5:
        result=1
    # print("dddddddddddddddddddddddd",imgObj.image.url)
    if pData == []:
        Results(rid=ridVal, phone=phone, date=date, result=result, pPhone = "", pNotes = "", dPhone = "").save()
    else:
        Results(rid=ridVal, phone=phone, date=date, result=result, pPhone = pData['pphone'], pNotes = "", dPhone = "").save()
    return result
    

def getPData(i):
    obj = Users.objects.filter(phone=i.pPhone).first()
    d = {'rid':i.rid,'date':i.date,'lung':i.lung,'heart':i.heart,'ratio':i.ratio,'result':i.result,'pName':obj.name,'pAge':obj.age, 'pContact':i.pPhone, 'pNotes':i.pNotes}
    return d

# def validPhone(phone):
#     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     if(re.fullmatch(regex, phone)):
#         return 1
#     else:
#         return 0


def valid(pData):
    if Users.objects.filter(phone=pData['pphone']).first() == None:
        return "Patient phone number is not registered with us! Please get them registered!"
    else:
        return 1


def validD(phone):
    if Users.objects.filter(phone=phone).first() == None:
        print("ohhhh", phone)
        return "Doctor phone is not registered with us! Please get them registered or check the number!!"
    else:
        return 1



def validPhone(phone, age):
    if not phone.isnumeric():
        return "Invalid Phone number, cannot give alphabets!"
    if not age.isnumeric():
        return "Invalid Age, age cannot contain alphabets!"
    return 1



def landing(request):
    # render(request, 'main/index.html')
    if request.POST:
        loginData = request.POST.dict()
        
        if 'name' in loginData.keys():
            if Users.objects.filter(phone=loginData['phone']).first() == None:
                # print(loginData['dob'])
                msg = validPhone(loginData['phone'], loginData['age'])
                if msg != 1:
                    return render(request, 'main/error.html', {'message':msg})
                Users(phone=loginData['phone'], name=loginData['name'], pwd=loginData['pwd'], age=loginData['age'], status=1, mode=loginData['mode']).save()
                request.session.create()
                request.session['phone'] = loginData['phone']
                request.session['mode'] = loginData['mode']
                return redirect('homePage')
            else:
                return render(request, 'main/error.html', {'message':'Account already exists!'})
                # return HttpResponse('<h1>Account already exists!</h1>')
        else:
            userObj=Users.objects.filter(phone=loginData['phone']).first()
            if userObj == None:
                return render(request, 'main/error.html', {'message':'Account not found!'})
                # return HttpResponse('<h1>Account not found!</h1>')
            else:
                if userObj.pwd == loginData['pwd']:
                    userObj.status=1
                    request.session.create()
                    request.session['phone'] = loginData['phone']
                    request.session['mode'] = userObj.mode
                    userObj.save()
                    return redirect('homePage')
                else:
                    return render(request, 'main/error.html', {'message':'Incorrect password!'})
                    # return HttpResponse('<h1>Incorrect password!</h1>')
    else:
        try:
            temp = request.session['phone']
            print(temp,'ttttttttttt')
            if temp != None:
                return redirect('homePage')
            return render(request, 'main/index.html')
        except:
            # print("fffffffffffffffffffffff")
            return render(request, 'main/index.html')


def home(request):
    if(request.POST):
        try:
            phone = request.session['phone']
            mode = request.session['mode']
            if phone == None:
                return redirect('landingPage')
        except:
            return redirect('landingPage')

        if 'logout' in request.POST:
            try:
                userObj=Users.objects.filter(phone=request.session['phone']).first()
                userObj.status=0
                userObj.save()
                request.session.flush()
                return redirect('landingPage')
            except:
                return redirect('landingPage')

        elif 'send' in request.POST:
            try:
                resultData = request.POST.dict()
                msg = validD(resultData['dphone'])
                if msg != 1:
                    return render(request, 'main/error.html', {'message':msg})
                result = Results.objects.filter(rid = resultData['rid']).first()
                result.dPhone = resultData['dphone']
                result.save()
                return render(request, 'main/success.html', {'message':"Successfully sent!"})
            except:
                return render(request, 'main/error.html', {'message':"Something went wrong :/ please try again!"})

        elif 'addnotes' in request.POST:
            try:
                resultData = request.POST.dict()
                result = Results.objects.filter(rid = resultData['rid']).first()
                result.pNotes = resultData['dnotes']
                result.save()
                return render(request, 'main/success.html', {'message':"Successfully sent!"})
            except:
                return render(request, 'main/error.html', {'message':"Something went wrong :/ please try again!"})

        elif 'pastresults' in request.POST:
            # try:
            resultObjs=Results.objects.filter(phone=phone)
            data = []
            for i in resultObjs:
                p = getPData(i)
                data.append(p)
            if resultObjs == None:
                return render(request, 'main/error.html', {'message':"Looks like you have no old results :/"})
                # return HttpResponse('<h1>Looks like you have no old results :/</h1>')
            data.reverse()
            
            d={'mode':mode, 'data':data}
            # print(docData[0].name)
            return render(request,'main/history.html',d)
            # except:
            #     return HttpResponse('<h1>some error in retreiving old results</h1>')


        elif 'imageBtn' in request.POST:
            # try:    
            date = str(datetime.now())
            ridVal = getHashValue(phone, date)
            imgObj = request.FILES['image']
            imgObj._name = ridVal+'.png'
            Images(rid=ridVal, image=imgObj).save()
            if mode == 'p' or mode == 'd':
                pData = []
            else:
                pData = request.POST.dict()
            print(pData)
            msg = valid(pData)
            if msg != 1:
                return render(request, 'main/error.html', {'message':msg})
            if checkCardiomegaly(ridVal, phone, date, pData):
                return render(request, 'main/error.html', {'message':"Tested POSITIVE for cardiomegaly!"})
            else:
                return render(request, 'main/success.html', {'message':"Tested NEGATIVE for cardiomegaly!"})
            # except:
            #     return render(request, 'main/error.html', {'message':"Something went wrong :/ Please try again!"})
        elif 'inbox' in request.POST:
            try:
                phone = request.session['phone']
                mode = request.session['mode']
                if mode == 'p':        
                    pData = Results.objects.filter(pPhone = phone)
                    # print('aaaaaaaaaaa')
                    data = []
                    for i in pData:
                        if i.pNotes != "":
                            data.append(i)           
                    # print(data,'ggggggggggg')
                    if data != []:
                        data.reverse()
                        d={'mode':request.session['mode'], 'data':data}
                        # return render(request, 'main/home.html', {'mode':request.session['mode']})
                        return render(request,'main/history.html',d)
                    else:
                        # return render(request, 'main/home.html', {'empty':1})
                        return render(request, 'main/error.html', {'message':"Inbox Empty!"})
                elif mode == 'd':
                    pData = Results.objects.filter(dPhone = phone)
                    data = []
                    for i in pData:
                        p = getPData(i)
                        data.append(p)
                    if data != []:
                        data.reverse()
                        d={'mode':request.session['mode'], 'data':data}
                        return render(request,'main/history.html',d)
                    else:
                        return render(request, 'main/error.html', {'message':"Inbox Empty!"})
                        # return render(request, 'main/home.html', {'empty':1})
                else:
                    return redirect('landingPage')
            except:
                return redirect('landingPage')
        elif 'docs' in request.POST:
            try:
                phone = request.session['phone']
                mode = request.session['mode']
                if mode == "t":
                    return redirect('docPage')
                else:
                    return redirect('landingPage')
            except:
                return redirect('landingPage')       

        
    else:
        try:
            temp = request.session['phone']
            print(temp,'llllllllllllll')
            if temp != None:
                print("hhh")
                d={'mode':request.session['mode']}
                return render(request, 'main/home.html',d)
            return redirect('landingPage')
        except:
            return redirect('landingPage')

    
def docs(request):
    if(request.POST):
        return redirect('homePage')
    else:
        docData = []
        doctors = Users.objects.filter(mode="d")
        for doc in doctors:
            docData.append(doc)
        d={'data':docData}
            # print(docData[0].name)
        return render(request,'main/docs.html',d)



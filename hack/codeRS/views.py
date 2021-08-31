# Create your views here.

from io import FileIO
from sys import path
from django.db.models import constraints
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect
from .forms import UsersSignupForm, UsersLoginForm
from customauth.models import MyUser
from codeRS.models import Solved, Problem
import datetime
import os
import pickle
import subprocess
from .thread import *

months = {
  1:'Jan',
  2:'Feb',
  3:'Mar',
  4:'Apr',
  5:'May',
  6:'June',
  7:'July',
  8:'Aug',
  9:'Sep',
  10:'Oct',
  11:'Nov',
  12:'Dec'
}

def test(request):
    print(request.POST)
    return HttpResponse('<h1>Yugi Muto</h1>')

def pending(request):
    return HttpResponse('<h1>This feature is yet to be implemented</h1>')

def sign(request):
    if request.method == 'POST':

        # user form
        form = UsersSignupForm(request.POST)

        # does form contains valid data
        if form.is_valid()==True:

            # if user already exists
            if form.is_already_present() == True:
                messages.error(request,'User with this email id already exists')

            else:
                first_name = form.cleaned_data['name'].split()[0]
                try:
                    last_name =  form.cleaned_data['name'].split()[1]
                except IndexError:
                    last_name = ''
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # creating new user
                usr = MyUser.objects.create_user(
                password = password,
                email = email,
                fname = first_name,
                lname = last_name,
                )
                usr.save()
                try:
                    os.mkdir('users/'+email)
                except FileExistsError:
                    print('New folder not created \nFolder already exists')
                messages.success(request,'Account created Successfully. You can login low..')
        else:
            messages.error(request,'Error in one or more form fields') 
    else:
        form = UsersSignupForm()
    return render(request,'codeRS/sign.html')

def dashboard(request):
    if request.user.is_anonymous:
        return redirect("/login/")

    # problems completed for python and C++
    cpp_completed = len(Solved.objects.filter(pid__language='cpp',uid=request.user.id))
    py_completed = len(Solved.objects.filter(pid__language='python',uid=request.user.id))

    # total number of problems
    py_total = len(Problem.objects.filter(language='python'))
    cpp_total = len(Problem.objects.filter(language='cpp'))

    # how much percentage meter to fill
    try:
        cpp_per = int((cpp_completed/cpp_total)*100)
    except ZeroDivisionError:
        cpp_per = 0
    
    try:
        py_per = int((py_completed/py_total)*100)
    except ZeroDivisionError:
        py_per=0

    global months
    xValues = []
    yValues = []

    # todays data
    today = datetime.date.today()

    # problems solved per day
    for i in range(7):
        date = today - datetime.timedelta(days=i)
        problems_solved = Solved.objects.filter(time=date,uid=request.user.id)
        yValues.insert(0,len(problems_solved))
        if i>1:
            xValues.insert(0,str(date.day) + '-' + months[date.month])
        elif i == 0:
            xValues.insert(0,'Today')
        else:
            xValues.insert(0,'Yesterday')
    
    return render(request,'codeRS/index.html',{'x':xValues,'y':yValues,'cppPer':cpp_per,'pyPer':py_per})

def login_(request):
    if request.method == 'POST':
        form = UsersLoginForm(request.POST)

        # checking if form fields contains valid data
        if form.is_valid()==True:

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # authenticating users
            usr = authenticate(request,email = email,password=password)
            if usr is not None:
                login(request,usr)
                request.session['email'] = email
                return redirect('/dashboard/')

            messages.error(request,'Invalid credentials')
    return render(request,'codeRS/login.html')

def logout_(request):
    messages.success(request,'Logged out successfully')
    logout(request)
    return redirect("/login/")

def problems(request):
    if request.user.is_anonymous:
        return redirect("/login/")

    if request.method == 'GET' :
        lang = 'cpp'
        try:
            id_ = request.GET['id']
            if id_ == '1':
                All_unsolved = showProblem(request,'cpp')
                lang = 'cpp'
            elif id_ == '2':
                All_unsolved = showProblem(request,'python')
                lang = 'python'
            else:
                messages.error(request,'Bad request')
                logout_(request)
                return redirect('/login/')
            return render(request,'codeRS/questions.html',{'problems':All_unsolved,'language':lang})
        except KeyError:
            return redirect('/dashboard/')

    return redirect('/dashboard/')

def showProblem(request,lang):
    Solved_ids = Solved.objects.filter(pid__language=lang,uid = request.user.id)
    All_unsolved = Problem.objects.filter(language=lang)
    return All_unsolved

'''This view function is of no use'''
def showSignupForm(request):
    if request.method == 'POST':
        fm = UsersSignupForm(request.POST)
        if fm.is_valid()==True:
            print('First Name: ',fm.cleaned_data['first_name'])
            print('Last Name: ',fm.cleaned_data['last_name'])
            print('Password: ',fm.cleaned_data['password'])
            print('Email: ',fm.cleaned_data['email'])
    else:
        fm = UsersSignupForm()
    return render(request,'signup.html',{'form':fm})

def update(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    if request.method == 'POST':
        id =  request.GET.get('id',' ')
        isValidId = id in [ str(problem.id) for problem in Problem.objects.all() ]

        if isValidId == False:
            messages.error(request,'Bad Request')
            logout_(request)
            return redirect('/login/')

        cwd = os.getcwd()
        sep = os.sep
        submissionPath = cwd + sep + 'users' + sep + request.user.email + sep + id
        with open(submissionPath + sep + 'pickle.dat','rb') as f:
            testCasesContainer = pickle.load(f)
        for i in range(testCasesContainer.numOfTestCases):
            print(testCasesContainer.testCases[i].status,testCasesContainer.testCases[i].output,testCasesContainer.testCases[i].expectedOutput)
        return render(request,'codeRS/codeProcessing.html',{'testCasesContainer':testCasesContainer})


def code(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    if request.method == 'GET' or request.method == 'POST': 
        try:
            id =  request.GET.get('id',' ')
            isValidId = id in [ str(problem.id) for problem in Problem.objects.all() ]

            if isValidId == False:
                messages.error(request,'Bad Request')
                logout_(request)
                return redirect('/login/')

            numTestCases = False
            problem = Problem.objects.get(pk=int(id))
            id_ = id
            cwd = os.getcwd()
            sep = os.sep

            # folder of manage.py file --> problems --> problemID  
            problemPath = cwd + sep +'problems' + sep + id
            with open(problemPath + sep + 'starter.txt','r') as f:
                starter = f.read()

            extension = 'cpp'
            if problem.language == 'python':
                extension = 'py'
            print('before post')
            if request.method == 'POST':
                # folder of manage.py file --> users --> 'test@gmail.com' --> problemID  
                submissionPath = cwd + sep + 'users' + sep + request.user.email + sep + id
                language = problem.language

                
                # file name of submitted file
                fileName = 'submit.' + extension

                # submitted code taken from ('code written')
                submittedCode = request.POST.get('code-written','')
                
                # folder of manage.py file --> users --> 'test@gmail.com' --> problemID --> submit  
                submittedFile = submissionPath + sep + fileName
                
                # folder of manage.py file --> users --> 'test@gmail.com' --> problemID --> out.txt 
                outputFile = submissionPath + sep + 'out.txt'
                print(outputFile)
                print('Before output file')


                print('Before os.oath')
                # code written into file named submit
                if os.path.isdir(submissionPath) == False:
                    os.mkdir(submissionPath)
                with open(submittedFile,'w') as f:
                    f.write(submittedCode)

                with open(outputFile,'w') as f:
                    pass
                
                # folder of manage.py file --> problems --> problemID --> TestCases  
                testCasesFolder = problemPath + sep + 'TestCases'
                
                # folder of manage.py file --> problems --> problemID --> TestCases --> test.txt
                testCasesInput = testCasesFolder + sep + 'test.txt'
                with open(testCasesInput,'r') as f:
                    rawInputList = f.read().split()

                # folder of manage.py file --> problems --> problemID --> TestCases --> ref.txt
                with open(testCasesFolder + sep + 'ref.txt','r') as f:
                    trueOutputList = f.read().splitlines()
                numTestCases  = len( trueOutputList )
                
                # emptying the existing file if any
                with open(submissionPath + sep + 'pickle.dat','wb') as f:
                    pass

                print(trueOutputList)

                if language == 'cpp':
                    compileRunCommand = 'g++ ' + submittedFile + ' -o ' + 'run && run < ' + testCasesInput + ' > ' + outputFile
                else:
                    compileRunCommand = 'python ' + submittedFile + ' < ' + testCasesInput + ' > ' + outputFile
                
                # compiling the submitted code
                process =  subprocess.Popen(compileRunCommand, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                
                # communicating with subprocess to get info about error
                (output, err) = process.communicate()
                err = err.decode('utf8').replace(submissionPath+sep,'')
                
                # whether process finished properly or not
                processStatus = process.wait()

                testCaseSize = int(( len(rawInputList)-1 )/numTestCases)
                # print('Raw input: ',rawInputList)
                
                # split the input based on testCaseSize
                j = 1
                inputList = []
                for i in range(numTestCases):
                    inputList.append(rawInputList[j:j + testCaseSize])
                    j = j + testCaseSize

                with open(outputFile,'r') as f:
                    userOutputList = f.read().splitlines()

                #print('input list: ',inputList)
                testCasesContainer = TestCases(numTestCases)
                testCasesContainerDummy = TestCases(numTestCases) 
                for i in range(numTestCases):
                    testCase = TestCase()
                    testCase.input = inputList[i]
                    testCase.expectedOutput = trueOutputList[i]
                    try:
                        testCase.output = userOutputList[i]
                    except IndexError:
                        print('No output')
                    testCasesContainer.testCases.append(testCase)


                    
                for i in range(numTestCases):
                    testCase = TestCase()
                    testCase.input = inputList[i]
                    testCase.expectedOutput = trueOutputList[i]
                    try:
                        testCase.output = userOutputList[i]
                    except IndexError:
                        print('No output')
                    testCasesContainerDummy.testCases.append(testCase)

                if processStatus == 1:
                    messages.error(request,'Compilation Error')
                    messages.info(request,err)

                    rangeListTemplate = [ i for i in range(numTestCases) ]
                    return render(request,'codeRS/error.html',
                                                {'testCasesContainer':testCasesContainerDummy,
                                                'range':rangeListTemplate})
                else:
                    messages.success(request,'Compiled Successfully')
                    
                    # getting list of outputs generated from user code


                    # size of each test case

                    


                            
                    with open(submissionPath + sep + 'pickle.dat','wb') as f:
                        pickle.dump(testCasesContainer,f)
                    # print(testCasesContainer)
                    # for i in range(numTestCases):
                    #     print(testCasesContainer.testCases[i].input,testCasesContainer.testCases[i].output)
                    CodeProcessor(testCasesContainer,submissionPath,id,request.user).run()

                    return render(request,'codeRS/codeProcessing.html',{'testCasesContainer':testCasesContainerDummy,'first':True})

                
            key = problem.impKey
            
            desc = problem.description.replace('<'+key+'>',"<div class='desc-back'>")
            desc = desc.replace('</'+key+'>','</div>')

            sampleOut = problem.example.replace('<'+key+'>',"<div class='desc-back'>")
            sampleOut = sampleOut.replace('</'+key+'>','</div>')

            iFormat = problem.inputf.replace('<'+key+'>',"<div class='desc-back'>")
            iFormat = iFormat.replace('</'+key+'>','</div>')

            oFormat = problem.outputf.replace('<'+key+'>',"<div class='desc-back'>")
            oFormat = oFormat.replace('</'+key+'>','</div>')

            constraints = problem.contraints 

            explanation = problem.explanation.replace('<'+key+'>',"<div class='desc-back'>")
            explanation = explanation.replace('</'+key+'>','</div>')
            return render(request,'codeRS/code.html',{
                'starter':starter,
                'problem':problem,
                'description':desc,
                "example":sampleOut,
                'inputf':iFormat,
                'outputf':oFormat,
                'constraints':constraints,
                'explanation':explanation,
                'numTestCases':numTestCases,
                'extension':extension
                })
        except FileNotFoundError:
            print('file nhi mili mereko')
            

    return render(request,'codeRS/code.html')

def download_csv(request):
    if request.user.is_anonymous:
        messages.warning(request,'You are not allowed to access this page')
        logout_(request)
        return redirect('/login/')

    if request.user.is_admin:
        f = open(os.getcwd()+os.sep+'data'+os.sep+'data.csv','w')
        dates = Solved.objects.order_by().values_list('time').distinct()
        users = Solved.objects.values_list('uid').distinct()
        for date in dates:
            for user in users:
                row = Solved.objects.filter(uid = user[0], time=date[0])
                for val in row:
                    f.write(str(val.pid.id)+',')
                if row:
                    f.write('\n')
        f.close()

        if os.path.exists(os.getcwd()+os.sep+'data'+os.sep+'data.csv'):
            with open(os.getcwd()+os.sep+'data'+os.sep+'data.csv', 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(os.getcwd()+os.sep+'data'+os.sep+'data.csv')
                return response
        raise Http404  

    messages.warning(request,'You are not allowed to access this page')
    logout_(request)
    return redirect('/login/')
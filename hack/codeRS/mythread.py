import threading
from customauth.models import MyUser
from codeRS.models import Solved, Problem

class CodeProcessor(threading.Thread):
	def __init__(self,request):
		threading.Thread.__init__(self)
		self.waiting = []
		self.success = []
		self.failed = []
		self.request = request

	def run(self):
		if request.user.is_anonymous:
			return redirect("/login/")
	    if request.method == 'GET' or request.method == 'POST': 
	        try:
	            test_bubble = False
	            print('See noi: ',os.getcwd())
	            id_ =  request.GET['id']
	            path_problem = os.getcwd()+os.sep+'problems'+os.sep+str(id_)
	            run_path = path_problem + os.sep + 'run.exe'
	            out_path = path_problem + os.sep + 'out.txt'
	            f = open(path_problem+os.sep+'starter.txt','r')
	            starter = f.read()
	            f.close()
	            if request.method == 'POST':
	                fname=''
	                test_bubble = True
	                code_content = request.POST.get('task','')
	                if Problem.objects.get(pk=int(id_)).language == 'cpp':
	                    fname='submit.cpp'
	                else:
	                    fname='submit.py'
	                f_code = open(path_problem + os.sep + fname,'w')
	                f_code.write(code_content)
	                f_code.close()
	                test_folder_path = path_problem + os.sep + 'TestCases'
	                testfile_path = path_problem + os.sep + 'TestCases' + os.sep + 'test.txt'
	                is_compile_sucess = False
	                if Problem.objects.get(pk = int(id_)).language=='cpp':
	                    status = os.system('g++ ' + path_problem + os.sep + fname +' -o ' + run_path)
	                    if status == 1:
	                        messages.error(request,'Compilation error occurred')
	                    else:
	                        messages.success(request,'Compiled Successfully')
	                        is_compile_sucess = True
	                        print(run_path)
	                        print(testfile_path)
	                        print(out_path)
	                        os.system(run_path + '< ' + testfile_path + ' >' + out_path)
	                elif Problem.objects.get(pk = int(id_)).language=='python':
	                    status = os.system('python ' + path_problem + os.sep + fname + '< '+ testfile_path + ' >' + out_path)
	                    if status == 1:
	                        messages.error(request,'Compilation error occurred')
	                    else:
	                        is_compile_sucess = True
	                        messages.success(request,'Compiled Successfully')
	                if is_compile_sucess:
	                    f_ref = open(test_folder_path + os.sep + 'ref.txt','r')
	                    ref_list = f_ref.read().splitlines()
	                    f_ref.close()

	                    f_out = open(out_path,'r')
	                    output_list = f_out.read().splitlines()
	                    f_out.close()

	                    for i in range(len(ref_list)):
	                        try:
	                            ref = ref_list[i]
	                            out = output_list[i]
	                            if ref == out:
	                                print(' Output ',i, 'passed')
	                            else:
	                                print('MISMATCH')
	                        except IndexError:
	                            print('Mismatch')
	                    if ref_list == output_list:
	                        User = MyUser.objects.get(pk=request.user.id)
	                        User.score += Problem.objects.get(pk=int(id_)).score
	                        User.save()

	                        solved = Solved(uid = request.user, pid = Problem.objects.get(pk=int(id_)))
	                        solved.save()

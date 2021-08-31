import threading
import os
import pickle
from .models import *
from django.contrib import messages
from django.shortcuts import render

class TestCases:
	def __init__(self,numOfTestCases):
		self.numOfTestCases = numOfTestCases
		self.processed = 0
		self.testCases = []

class TestCase:
	def __init__(self):
		self.status = 2
		self.input = []
		self.expectedOutput = []
		self.output = []

class CodeProcessor(threading.Thread):
	def __init__(self,testCasesContainer,submissionPath,pid,user):
		self.pid = pid
		self.User = user
		self.testCasesContainer = testCasesContainer
		self.submissionPath = submissionPath
		threading.Thread.__init__(self)

	def run(self):
		self.count = 0
		with open(self.submissionPath + os.sep + 'pickle.dat','wb+') as f:
			for i in range(self.testCasesContainer.numOfTestCases):
				if self.testCasesContainer.testCases[i].output == self.testCasesContainer.testCases[i].expectedOutput: 
					self.testCasesContainer.testCases[i].status = 0
					self.count += 1
				else:
					self.testCasesContainer.testCases[i].status = 1
				self.testCasesContainer.processed += 1
				pickle.dump(self.testCasesContainer,f)
				f.seek(0)
				print('Processed {}'.format(i),self.testCasesContainer.testCases[i].status)
		
		if self.count == self.testCasesContainer.numOfTestCases:
			User = MyUser.objects.get(pk=self.User.id)

			if len(Solved.objects.filter(uid=self.User, pid = Problem.objects.get(pk=int(self.pid)))) == 0:
				User.score += Problem.objects.get(pk=int(self.pid)).score
				User.save()

				solved = Solved(uid = self.User, pid = Problem.objects.get(pk=int(self.pid)))
				solved.save()
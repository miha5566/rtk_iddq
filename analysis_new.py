#analysis_new.py

# recreate on 2015/10/23
# take iddq datas from the input and analysis


import re
import sys

import numpy as np

#from sklearn import svm

import plotting_new # plotting results
import fileIO_new


#####################################################################
#Function Definition
#####################################################################

def num(s):
	if s != '':
		try:
			return int(s)
		except ValueError:
			return float(s)
	else: 
		return False
		
def not_emp(itemlist): #?????????????
	count = 0
	for item in itemlist:
		if item != "":
			count += 1
	return count
	
def GetTopN(idlist,xlist,ylist,valuelist,rank):
	indices = np.argpartition(valuelist,-rank)[-rank:]
	ID_ans = idlist[indices]
	X_ans = xlist[indices]
	Y_ans = ylist[indices]
	Value_ans = valuelist[indices] #sort by this
	X_ans = np.array([x for (v,x) in sorted(zip(Value_ans,X_ans))])
	Y_ans = np.array([y for (v,y) in sorted(zip(Value_ans,Y_ans))])
	ID_ans = np.array([i for (v,i) in sorted(zip(Value_ans,ID_ans))])
	Value_ans.sort() #finish sorting
	
	return (ID_ans,X_ans,Y_ans,Value_ans)

def outlier(vlist,value): # only for absolute values
	std_dev = np.std(vlist)
	mean = np.average(vlist)
	if value > mean+3*std_dev:
		return True
	else:
		return False
		
def dual_cluster(vlist):
	std_dev = np.std(vlist)
	mean = np.average(vlist)
	max_value = max(vlist)
	min_value = min(vlist)
	vlist.sort()
	index = int(len(vlist)*0.9)
	quarter3 = vlist[index]
	if max_value < (mean + 2.5 * std_dev) and max_value >10 :# min_value > (mean - 2.5* std_dev):
	#if max_value > 10 and quarter3 > (mean + 2 * std_dev):
		return True
	else:
		#if max_value < 0.5:
		#	return True
		#else
		return False
	
	
def judgeDies(idlist,xlist,ylist,vlist):
	ans_idlist = np.array([]) 
	ans_xlist = np.array([]) 
	ans_ylist = np.array([]) 
	ans_vlist = np.array([]) 
	for ID,x,y,v in zip(idlist,xlist,ylist,vlist):
		if outlier(vlist,v):
			ans_idlist = np.append(ans_idlist,ID)
			ans_xlist = np.append(ans_xlist,x)
			ans_ylist = np.append(ans_ylist,y)
			ans_vlist = np.append(ans_vlist,v)
	ans_xlist = np.array([x for (v,x) in sorted(zip(ans_vlist,ans_xlist))])
	ans_ylist = np.array([y for (v,y) in sorted(zip(ans_vlist,ans_ylist))])
	ans_idlist= np.array([i for (v,i) in sorted(zip(ans_vlist,ans_idlist))])
	ans_vlist.sort() #finish sorting
	
	return (ans_idlist,ans_xlist,ans_ylist,ans_vlist)
	
	
def difference(i_values,i_nums,i_names): ## number of mode is not right , need to fix
	
	d_values = np.diff(i_values)
	il = [(num,name) for num ,name in zip(i_nums[0:-1],i_names[0:-1])]
	ir = [(num,name) for num ,name in zip(i_nums[1:],i_names[1:])]

	return il,ir,d_values
	
#####################################################################
#Input Setting - convert to useful format
#####################################################################

infileName = sys.argv[1]
all_die_list ,all_name_list ,all_num_list = fileIO_new.Read(infileName)

outfileName = infileName.strip('.csv')+'_result.txt'

#####################################################################
#Data Processing
#####################################################################
#iteratively check 

TestList = {}
TestIsDelta = {}
TestMode = {}
TestNameList = {}

for name,number in zip(all_name_list,all_num_list):
	TestList.update({(num(number),name):np.array([])})
	
#	TestIsDelta.update({num(number):None})
#	TestMode.update({num(number):None})
	
deleteSet = set()

XList = np.array([])
YList = np.array([])
AvgAllList = np.array([])
MaxAllList = np.array([])
SiteList = np.array([])
IDList = np.array([])
IAvgList = np.array([])
IStdList = np.array([])
IMaxList = np.array([])
MaxModeList = {}

bad_pattern_exist = True
First = True

#iterModeCount = modeCount.copy()

#iter0_Threshold = None
#iter0_wrongDies = None
#iter0_wrongDies2= None


Round = 0
while bad_pattern_exist: # iterative loop
	# clear the pattern pool
	print('round:%d'%Round)

	D_Test_List = {}
	iterDeleteSet = set()
#	DeltaAll = np.array([])
#	IddqAll =  np.array([])
#	IddqNumberAll = np.array([])
	
	XList = np.array([])
	YList = np.array([])
	AvgAllList = np.array([])
	MaxAllList = np.array([])
	SiteList = np.array([])
	IDList = np.array([])
	IAvgList = np.array([])
	IStdList = np.array([])
	IMaxList = np.array([])
	MaxModeList = {}
	
	for ID in all_die_list:
		die = all_die_list[ID]
		#clear all lists
		
		IddqAll =  np.array([])
		DeltaAll = np.array([])
		IddqL = []
		IddqR = []
		IddqNumNameAll = []
		
		DeltaByMode = {} ######################################### could be optimized
		
		for mode in die['Mode']:
			#print('%d:%d'%(ID,mode))
			for name,num,value in zip(die[int(mode)]['Name'],die[int(mode)]['Num'],die[int(mode)]['Value']):

				if len(deleteSet.intersection({(num,name)}))==0:
					IddqNumNameAll.append((num,name))
					IddqAll=np.append(IddqAll,value)

					if First: 
						TestList[(num,name)] = np.append(TestList[(num,name)],value)
						
			DeltaByMode.update({mode:{'Il':None,'Ir':None,'Value':None}})	
			DeltaByMode[mode]['Il'],DeltaByMode[mode]['Ir'],DeltaByMode[mode]['Value']\
			=difference(die[mode]['Value'],die[mode]['Num'],die[mode]['Name'])	
			DeltaAll = np.append(DeltaAll,DeltaByMode[mode]['Value'])	
			IddqR.extend(DeltaByMode[mode]['Ir'])
			IddqL.extend(DeltaByMode[mode]['Il'])			
		
		if len(DeltaAll)!=0 and len(IddqAll)!=0:
			for il,ir,dvalue in zip(IddqL,IddqR,DeltaAll) :
				try:
					D_Test_List[(il,ir)]=np.append(D_Test_List[(il,ir)],dvalue)
				except:					
					D_Test_List.update({(il,ir):np.array([dvalue])})

				
			IDList = np.append(IDList,ID)
			XList = np.append(XList ,die['X'])
			YList = np.append(YList ,die['Y'])
			SiteList = np.append(SiteList ,die['HwBin'])
			AvgAllList = np.append(AvgAllList ,np.average( np.array([abs (i) for i in DeltaAll])) )
			MaxAllList = np.append(MaxAllList ,max([abs(i) for i in DeltaAll])) 
			IAvgList = np.append(IAvgList,np.average(np.array([abs(i) for i in IddqAll])))
			IStdList = np.append(IStdList,np.std(np.array([abs(i) for i in IddqAll])))
			IMaxList = np.append(IMaxList,np.max(np.array([abs(i) for i in IddqAll])))
			for mode in DeltaByMode:
				try:
					MaxModeList[mode]['Dmax'] = np.append(MaxModeList[mode]['Dmax'],max([abs(i) for i in DeltaByMode[mode]['Value']]))
					MaxModeList[mode]['Imax'] = np.append(MaxModeList[mode]['Imax'],max([abs(i) for i in die[mode]['Value']]))
					MaxModeList[mode]['X'] = np.append(MaxModeList[mode]['X'],die['Y'])
					MaxModeList[mode]['Y'] = np.append(MaxModeList[mode]['Y'],die['X'])
					MaxModeList[mode]['ID'] = np.append(MaxModeList[mode]['ID'],ID)
				except:
					MaxModeList.update({mode:{'Dmax':np.array([max([abs(i) for i in DeltaByMode[mode]['Value']])]),\
					'Imax':np.array([max([abs(i) for i in die[mode]['Value']])]),\
					'X':np.array([die['Y']]),\
					'Y':np.array([die['X']]),\
					'ID':np.array(ID)}})		
			

	# deleting patterns
	I_number_list = []
	I_name_list = []
	
	for il,ir in D_Test_List:
		vlist = D_Test_List[(il,ir)]
		if dual_cluster(abs(vlist)):
			
			if np.average(vlist)<0:
				del_test = ir #left iddq pattern
			else:
				del_test = il #right iddq pattern
			iterDeleteSet.add(del_test)

	print(deleteSet)
	deleteSet = deleteSet.union(iterDeleteSet)
	
	#plotting2.saveChosenIddqPatterns(TestList,deleteSet,infileName)
	
	First = False if First else First
	bad_pattern_exist = True if len(iterDeleteSet) > 0 else False
	#####	save figures
	plotting_new.saveFigures(IMaxList,MaxAllList,Round,infileName)
	for m in MaxModeList:
		plotting_new.saveFigures(MaxModeList[m]['Imax'],MaxModeList[m]['Dmax'],Round,infileName,m)
	
	#plotting_new.saveDeltaPatterns(D_Test_List,Round,NumNames=False,fileName=infileName)
	#####	save figures

	Round+=1





#####################################################################
#Output results
#####################################################################

wrongDies=judgeDies(IDList,XList,YList,MaxAllList)

#print (TestList)
#plotting_new.savePatterns(TestList,infileName)
modeWrongDies = {}
modeThreshold = {}
for m in MaxModeList :
	d_vlist = MaxModeList[m]['Dmax']
	i_vlist = MaxModeList[m]['Imax']
	x_list = MaxModeList[m]['X']
	y_list = MaxModeList[m]['Y']
	id_list = MaxModeList[m]['ID']
	modeWrongDies.update({m:judgeDies(id_list,x_list,y_list,d_vlist)})
	modeThreshold.update({m:np.average(d_vlist)+3*np.std(d_vlist)})
	fileIO_new.Output(infileName.strip('.csv')+'_out.txt',deleteSet,wrongDies,modeWrongDies,modeThreshold,TestList)
	

	








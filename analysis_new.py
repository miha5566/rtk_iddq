#analysis_new.py

# recreate on 2015/10/23
# take iddq datas from the input and analysis

import re
import sys

import numpy as np
#import scipy as sp
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

def outlier(vlist,value): # only for judgeDies
    
    std_dev = np.std(vlist)
    mean = np.average(vlist)
    if value>0:
        return value > mean+3*std_dev #or value < mean-3*std_dev:
    elif value<0:
        return value < mean-3*std_dev
    else :
        return False
		
def dual_cluster(vlist):
	std_dev = np.std(vlist)
	mean = np.average(vlist)
	max_value = max(vlist)
	min_value = min(vlist)
	vlist.sort()
	
	#index3 = int(len(vlist)*0.25)
	#index1 = int(len(vlist)*0.75)
	#qr3 = vlist[index3]
	#qr1 = vlist[index1]
	#iqr = abs(qr3 - qr1)
	
	v1 = vlist[int(len(vlist)*0.067)]
	v2 = vlist[int(len(vlist)*0.933)]
	e1 = mean - 1.5 *std_dev
	e2 = mean + 1.5 *std_dev
	#print('iqr:%f|sd:%f'%(iqr,std_dev))
	if max_value < (mean + 3 * std_dev) and min_value > (mean - 3* std_dev):#and max_value >10 :# 
	
	# SD > IQR/1.35 => HEAVY TAIL
	# SD < IQR/1.35 => LIGHT TAIL
	# SD = IQR/1.35 => NORMAL
	#print('e1:%f|v1:%f'%(e1,v1))
	#print('e2:%f|v2:%f'%(e2,v2))
	#if abs(e1-v1)>0.5*std_dev and abs(e2-v2)>0.5*std_dev : # exceed 10%
		return True
	else:
		#if max_value < 0.5:
		#	return True
		#else
		return False
		
def isNormalLinear(vlist,interval_num):
    std_dev = np.std(vlist)
    mean = np.average(vlist)
    max_value = max(vlist)
    min_value = min(vlist)
    
    vlist.sort()
    normalvlist = np.random.normal(mean,std_dev,len(vlist))
#    MAX = 
#    CDFM = 
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
	
def judgeDiesNeg(idlist,xlist,ylist,vlist):
	ans_idlist = np.array([]) 
	ans_xlist = np.array([]) 
	ans_ylist = np.array([]) 
	ans_vlist = np.array([])
	
	for ID,x,y,v in zip(idlist,xlist,ylist,vlist):
		if v < np.average(vlist)-3*np.std(vlist):
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

	#for dv,ilnn,irnn in zip(d_values,il,ir):
	#	if dv>10:
	#		print (dv)
	#		print(ilnn)
	#		print(irnn)
	
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
deleteSet_parent = set()


XList = np.array([])
YList = np.array([])
AvgAllList = np.array([])
MaxAllList = np.array([])
MaxNegList = np.array([])
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


lesscount = 0


while bad_pattern_exist: # iterative loop
	# clear the pattern pool
	print('round:%d'%Round)

	D_Test_List = {}
	ID_Test_List = {}
	
	iterDeleteSet = set()
	
#	DeltaAll = np.array([])
#	IddqAll =  np.array([])
#	IddqNumberAll = np.array([])
	
	XList = np.array([])
	YList = np.array([])
	AvgAllList = np.array([])
	MaxAllList = np.array([])
	MaxNegList = np.array([])
	SiteList = np.array([])
	IDList = np.array([])
	IAvgList = np.array([])
	IStdList = np.array([])
	IMaxList = np.array([])
	MaxModeList = {}
	

	
	for ID in all_die_list:
		if ID==127:
		    continue
		die = all_die_list[ID]
		#clear all lists
		
		
		IddqAll =  np.array([])
		DeltaAll = np.array([])
		IddqL = []
		IddqR = []
		IddqNumAll = []
		IddqNameAll = []
		
		DeltaByMode = {} ######################################### could be optimized
		
		for mode in die['Mode']:
			#print('%d:%d'%(ID,mode))
			
			IddqMode =  np.array([])
			IddqNum = []
			IddqName = []
			for name,number,value in zip(die[int(mode)]['Name'],die[int(mode)]['Num'],die[int(mode)]['Value']):

				if len(deleteSet.intersection({(num,name)}))==0:
					IddqNum.append(number)
					IddqName.append(name)
					IddqMode=np.append(IddqMode,value)

					if First: 
						TestList[(number,name)] = np.append(TestList[(number,name)],value)
				#else:
				#	print("%d|%s"%(num,name))
						
			DeltaByMode.update({mode:{'Il':None,'Ir':None,'Value':None,'iValue':None}})	
			#DeltaByMode[mode]['Il'],DeltaByMode[mode]['Ir'],DeltaByMode[mode]['Value']\
			#=difference(die[mode]['Value'],die[mode]['Num'],die[mode]['Name'])	 ########################Never Done!!!
			
			DeltaByMode[mode]['Il'],DeltaByMode[mode]['Ir'],DeltaByMode[mode]['Value']\
			=difference(IddqMode,IddqNum,IddqName)	 ########################Why have 2 mode
			DeltaByMode[mode]['iValue'] = IddqMode
			
			DeltaAll = np.append(DeltaAll,DeltaByMode[mode]['Value'])	
			IddqAll = np.append(IddqAll,IddqMode)
				
			IddqR.extend(DeltaByMode[mode]['Ir'])
			IddqL.extend(DeltaByMode[mode]['Il'])
			
		if First:		
			#print(len(DeltaAll),end="|")
			#print(len(IddqAll))
			if len(IddqAll) < 208:
				lesscount += 1
		if len(DeltaAll)!=0 and len(IddqAll)!=0:
			for il,ir,dvalue in zip(IddqL,IddqR,DeltaAll) :
				try:
				    D_Test_List[(il,ir)]=np.append(D_Test_List[(il,ir)],dvalue)
				    ID_Test_List[(il,ir)]=np.append(ID_Test_List[(il,ir)],ID)
				except:					
				    D_Test_List.update({(il,ir):np.array([dvalue])})
				    ID_Test_List.update({(il,ir):np.array([ID])})

				
			IDList = np.append(IDList,ID)
			XList = np.append(XList ,die['X'])
			YList = np.append(YList ,die['Y'])
			SiteList = np.append(SiteList ,die['HwBin'])
			#AvgAllList = np.append(AvgAllList ,np.average( np.array([abs (i) for i in DeltaAll])) )
			
			DeltaPos = DeltaAll[DeltaAll>=0]
			DeltaNeg = DeltaAll[DeltaAll<0]
			
			
			try:
			    MaxAllList = np.append(MaxAllList ,max(DeltaPos)) 
			except:
			    MaxAllList = np.append(MaxAllList ,0) 
			try:
			    MaxNegList = np.append(MaxNegList ,min(DeltaNeg))
			except:
			    MaxNegList = np.append(MaxNegList ,0)
			    
			#IAvgList = np.append(IAvgList,np.average(np.array([abs(i) for i in IddqAll])))
			#IStdList = np.append(IStdList,np.std(np.array([abs(i) for i in IddqAll])))
			IMaxList = np.append(IMaxList,np.max(IddqAll))
			for mode in DeltaByMode:
				try:
					vl = DeltaByMode[mode]['Value']
					vn = vl[vl<0]
					vp = vl[vl>=0]
					pfill = 0 if len(vp)==0 else max(vp)
					nfill = 0 if len(vn)==0 else min(vn)
					MaxModeList[mode]['Dmax'] = np.append(MaxModeList[mode]['Dmax'],pfill)
					MaxModeList[mode]['Dmin'] = np.append(MaxModeList[mode]['Dmin'],nfill)
					MaxModeList[mode]['Imax'] = np.append(MaxModeList[mode]['Imax'],max(DeltaByMode[mode]['iValue']))
					MaxModeList[mode]['X'] = np.append(MaxModeList[mode]['X'],die['Y'])
					MaxModeList[mode]['Y'] = np.append(MaxModeList[mode]['Y'],die['X'])
					MaxModeList[mode]['ID'] = np.append(MaxModeList[mode]['ID'],ID)
				except:
					try:
						vl = DeltaByMode[mode]['Value']
						vp = vl[vl>=0]
						vn = vl[vl<0]
						pfill = 0 if len(vp)==0 else max(vp)
						nfill = 0 if len(vn)==0 else min(vn)
						MaxModeList.update({mode:{'Dmax':np.array([pfill]),\
						'Dmin':np.array([nfill]),\
						'Imax':np.array([max(DeltaByMode[mode]['iValue'])]),\
						'X':np.array([die['Y']]),\
						'Y':np.array([die['X']]),\
						'ID':np.array(ID)}})		
					except:
					    print("empty: ID",end="")
					    print(ID,end=" Mode")
					    print(mode)
			

	# deleting patterns
	I_number_list = []
	I_name_list = []
	
	for il,ir in D_Test_List:
		vlist = D_Test_List[(il,ir)]
		if dual_cluster(vlist): #determine abs
			
			if np.average(vlist)<0: #ir - il delete larger
				del_test = il #left iddq pattern
			else:
				del_test = ir #right iddq pattern
			iterDeleteSet.add(del_test)

	print(iterDeleteSet - deleteSet)
	#print(iterDeleteSet)
	
	
	#plotting2.saveChosenIddqPatterns(TestList,deleteSet,infileName)
	
	First = False if First else First
	bad_pattern_exist = True if len(iterDeleteSet - deleteSet) > 0 else False
	
	deleteSet = deleteSet.union(iterDeleteSet)
	#####	save figures
	
	#plotting_new.saveFigures(IMaxList,MaxAllList,Round,infileName)
	#for m in MaxModeList:
	#	plotting_new.saveFigures(MaxModeList[m]['Imax'],MaxModeList[m]['Dmax'],Round,infileName,m)
	#if Round ==0:
	#	plotting_new.saveDeltaPatterns(D_Test_List,Round,NumNames=False,fileName=infileName)
	
	#####	save figures
	
	if Round == 0:
	    for dInumname in D_Test_List:
	        il,ir = dInumname
	        ilnum,ilname = il
	        ilmode = num(ilname.strip('_iddq scan_IDDQ -1').strip('mode'))
	        irnum,irname = ir
	        irmode = num(irname.strip('_iddq scan_IDDQ -1').strip('mode'))
	        pool = [48,53]
	        if (ilnum in pool or irnum in pool )and irmode==8 and ilmode==8:
	            print('mode8 %d-%d'%(irnum,ilnum))
	            
	            std_dev = np.std(D_Test_List[dInumname])
	            mean =  np.average(D_Test_List[dInumname])
	            for ID,value in zip(ID_Test_List[dInumname],D_Test_List[dInumname]):
	                if value>mean+3*std_dev :
	                    print('big:%d'%ID,end='=>')
	                    print(value)
	                elif value<mean-3*std_dev :
        	            print('small:%d'%ID,end='=>')
        	            print(value)
	    
	Round+=1

print (lesscount,end = "/")
print (len(all_die_list),end = "=")
print (lesscount/len(all_die_list))


#####################################################################
#Output results
#####################################################################

wrongDies=judgeDies(IDList,XList,YList,MaxAllList)

#print (TestList)
#plotting_new.saveDeltaPatterns(D_Test_List,Round,NumNames=deleteSet,fileName=infileName)
#plotting_new.savePatterns(TestList,infileName)
#plotting_new.saveModeDies(all_die_list,infileName)
#plotting_new.observeMode8Dies(all_die_list,infileName)

modeWrongDies = {}
modeWrongDiesn = {}
modeThreshold = {}
modeThresholdn = {}
modeMean = {}
modeMeanN = {}

for m in MaxModeList :
	d_vlist = MaxModeList[m]['Dmax']
	d_vlist_n = MaxModeList[m]['Dmin']
#	pool = [0,2,4,6,3,8]
#	if m in pool:
#	    print ('mode%d'%m)
#	    print(d_vlist)
#	    print(d_vlist_n)
#	    print(np.average(d_vlist_n))
#	    print(np.std(d_vlist_n))
	i_vlist = MaxModeList[m]['Imax']
	x_list = MaxModeList[m]['X']
	y_list = MaxModeList[m]['Y']
	id_list = MaxModeList[m]['ID']
	modeWrongDies.update({m:judgeDies(id_list,x_list,y_list,d_vlist)})
	modeWrongDiesn.update({m:judgeDies(id_list,x_list,y_list,d_vlist_n)})
	modeThreshold.update({m:np.average(d_vlist)+3*np.std(d_vlist)})
	modeThresholdn.update({m:np.average(d_vlist_n)-3*np.std(d_vlist_n)})
	modeMean.update({m:np.average(d_vlist)})
	modeMeanN.update({m:np.average(d_vlist_n)})
fileIO_new.Output(infileName.strip('.csv')+'_out.txt',deleteSet,wrongDies,modeWrongDies,modeMean,modeThreshold,TestList)
fileIO_new.Output(infileName.strip('.csv')+'_n_out.txt',deleteSet,wrongDies,modeWrongDiesn,modeMeanN,modeThresholdn,TestList)


	








#read.py
# create on 2015/09/18
# read the iddq datas and return as useful format

import re
import csv
import numpy as np


def num(s):
	if s != '':
		try:
			return int(s)
		except ValueError:
			return float(s)
	else: 
		return False

def column_valid_name(name):
	isDelay = re.findall('delay',name)
	isDelta = re.findall('d_scan',name)
	d = True if isDelta else False # isdelta
	isi = False
	if not d and re.findall('scan',name) :
		isi = True
	m_tmp= re.findall('mode[0-9]+_iddq', name) 
	m_tmp2= re.findall('-1',name)
	m = num(m_tmp[0].strip("mode").strip("_iddq") ) if m_tmp and m_tmp2 else None# mode  
	return (m , m_tmp and m_tmp2 and isi and (not isDelay))
	
def column_valid_value(col): # take string
	e =  True if num(col)>10 and col.strip()!='' and col.strip()!='1' else False
	return e

def column_valid(index,namelist,col):
	#isDelay = re.findall('delay',namelist[index])
	#isDelta = re.findall('d_scan',namelist[index])
				
	#d = True if isDelta else False # isdelta
	#isi = False
	#if not d and re.findall('scan',namelist[index]) and num(col)>10:
	#	isi = True
	#m_tmp= re.findall('mode[0-9]+_iddq', namelist[index]) #######################
	#m_tmp2= re.findall('-1',namelist[index]) #######################
				
	#m = num( m_tmp[0].strip("mode").strip("_iddq") ) if m_tmp and m_tmp2 else None# mode  #######################
	#e = True if col.strip()!="" and col.strip() != "1" else False # exit
	
	m,vn = column_valid_name(namelist[index])
	vv = column_valid_value(col)
	
	return (m , vn and vv)
		
		
def Read(fileName,read_type=False):
	# global variables that would return 
	all_die_list = {}
	test_name_list = []
	test_num_list = []
	
	#modeCount = {}
	
	# read file and deal the input
	csvfile = open(fileName,'r')
	#rawDataStr = csvfile.read()
	#rawData = rawDataStr.split("\n")
	
	reader = csv.reader(csvfile)

	
	for i ,newitem in enumerate(reader): #newitem = row

		dieIDList = re.findall('id: [0-9]+ ',newitem[0].replace('\n',' '))
		dieXList = re.findall('X=[0-9]+',newitem[0].replace('\n',' '))
		dieYList = re.findall('Y=[0-9]+',newitem[0].replace('\n',' '))
		dieSiteList = re.findall('Site #: [0-9]+',newitem[0].replace('\n',' '))
		dieHwBinList = re.findall('HwBin: [0-9]+',newitem[0].replace('\n',' '))
		dieid = None
		dieX = None
		dieY = None
		dieSite = None

		IsNumList = newitem[0].replace('\n','') == "Test#"
		IsNameList = newitem[0].replace('\n','') == "Test name"
		IsSeqList = newitem[0].replace('\n','') == "Seq. name"
	
		if dieIDList :
			#print(newitem[0].replace('\n',' '))
			dieid = num(dieIDList[0].strip("id: ").strip())
			dieX = num(dieXList[0].strip("X="))
			dieY = num(dieYList[0].strip("Y="))
			dieSite = num(dieSiteList[0].strip("Site #: "))
			dieHwBin = num(dieHwBinList[0].strip("HwBin: "))

			new = {dieid :{'X':dieX,'Y':dieY,'HwBin':dieHwBin,'Site':dieSite,'Mode':set()}}
			
			modeValues = {}
			
				
			#datas = {	'isDelta':[],'isIddq':[],'Value':np.array([]),
			#			'Num':[],'Mode':[],'Name':[],'Exist':[]}
			
			 
			shift = 0
			last_m = None
			for raw_j, col in enumerate(newitem[1:]) :
				isDelay = re.findall('delay',test_name_list[raw_j])
				if re.findall('TDF',test_name_list[raw_j]) or isDelay:
					break #do not deal with delayed patterns
					
				##############################################################
				m, e = column_valid(raw_j,test_name_list,col)
				
				if m!=last_m and shift >0 :
					shift = 0 # new mode 
				last_m = m

				if not e:
					shift += 1
					continue
				
				j = raw_j - shift
				#print('%d|%d|%d|%d|%d'%(dieid,m,raw_j,j,shift))
				
				##############################################################

				#isDelta = re.findall('d_scan',test_name_list[j])
		
				m, v = column_valid(j,test_name_list,col) 
				
				#d = True if isDelta else False # isdelta
				#isi = False
				#if not d and re.findall('scan',test_name_list[j]) and num(col)>10:
				#	isi = True
				#m_tmp= re.findall('mode[0-9]+_iddq', test_name_list[j]) #######################
				#m_tmp2= re.findall('-1',test_name_list[j]) #######################
				
				#m = num( m_tmp[0].strip("mode").strip("_iddq") ) if m_tmp and m_tmp2 else False# mode  #######################
				#e = True if col.strip()!="" and col.strip() != "1" else False # exit
					
				if v and (m!=10 and m!=5 ): #we take m_tmp and m_tmp2 because m=0 is possible
					try:
						modeValues[m]['Name'].append(test_name_list[j])
						modeValues[m]['Num'].append(num(test_num_list[j]))
						modeValues[m]['Value'] = np.append(modeValues[m]['Value'],num(col) )
					except:
						modeValues.update({m:{'Name':[test_name_list[j]],'Num':[num(test_num_list[j])],'Value':np.array([num(col)]) }})
						new[dieid]['Mode'].add(m)
						
			new[dieid].update(modeValues)	
			all_die_list.update(new)
		

		elif IsNameList:
			test_name_list = newitem[1:]
		elif IsNumList:
			test_num_list = newitem[1:]
	
	
	#print(all_die_list)
	print(len(all_die_list))
	
	all_name_list = []
	all_num_list = []
	for number,name in zip(test_num_list,test_name_list):
		if re.findall('delay',name):
			break 
		m,v = column_valid_name(name)
		if v and (m!=10 and m!=5 ):
			#print (number+'|'+name)
			all_name_list.append(name)
			all_num_list.append(number)
			

	return (all_die_list,all_name_list,all_num_list)
	
	
def Output(	fileName,deleteSet,wrongDies,modeWrongDies,modeThreshold,TestList):
	outfile = open(fileName,'w')
	
	#patterns

	print('------Tests deleted:%d------'%len(deleteSet),file=outfile,end='\r\n')
	for num_name_tuple in list(deleteSet):
		num , name = num_name_tuple
		print('Number/Name:%d/%s\r\n\tMaximum:%f\r\n\tAverage:%f\r\n\tStandard Deviation:%f'
				%(int(num),name,
				np.max(abs(TestList[num_name_tuple])),
				np.average( abs(TestList[num_name_tuple]) ),
				np.std(abs(TestList[num_name_tuple])) )
				,file=outfile,end='\r\n')
	#dies
	
	#wrongID,wrongX,wrongY,wrongValue = wrongDies
	
#	print('------Iddq Threshold: %f(mA)------'%(ithreshold),file=outfile)
	for m in modeWrongDies:
		wrongID,wrongX,wrongY,wrongValue = modeWrongDies[m]
		print('\r\n',file=outfile)
		print('------MODE: %d------'%(m),file=outfile,end='\r\n')
		print('------Wrong dies (deleted): %d------'%len(wrongID),file=outfile,end='\r\n')
		print('------Delta Iddq Threshold: %f(mA)------'%(modeThreshold[m]),file=outfile,end='\r\n')
		
		for index,ID,wx,wy,wv in zip(range(len(wrongID)),wrongID,wrongX,wrongY,wrongValue):
			print('ID:%d\r\n\tMaximum Delta:%f\r\n\tLocation:(%d,%d)'
				%(int(ID),wv,int(wx),int(wy)) ,file=outfile,end='\r\n')

				
					
	outfile.close()	


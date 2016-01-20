#plotting.py
# create on 2015/09/18
# plotting the result from iddq datas

import numpy as np
import matplotlib.pyplot as plt

#####################################################################
#Plotting
#####################################################################
#Plotting modules definition

def subpltDieBarLine(
		Fig,pos,values,
		title,I_value,BarColor='red',
		LineColor ='blue',Xlabel='',Ylabel='(mA)',
		tx=False,ty=False,RefValue=False):
	ax = Fig.add_subplot(pos)
	axx = np.array([i+1 for i in range(len(values))])
	ax.bar(axx,values,width=0.8,color=BarColor)
	ax.plot(axx,values,color=LineColor)
	ax.set_title(title)
	ax.set_xlabel(Xlabel)
	ax.set_ylabel(Ylabel)
	if tx and ty:
		if RefValue:
			ax.text(tx,ty,RefValue+"\nmean of Iddq:%f"%I_value)
		else:
			ax.text(tx,ty,"mean of Iddq:%f"%I_value)

def subpltHist(
		Fig,pos,values,
		title,Color='blue',Xlabel='(mA)',
		Ylabel='Frequency',binnum=80,upperlimit=False,
		tx=False,ty=False,reverse_axis=False):

	w = ( (max(values)-min(values)) / binnum ) * 0.7
	try:
		ax = Fig.add_subplot(pos)
	except:
		try:
			p1,p2,p3=pos
			ax = Fig.add_subplot(p1,p2,p3)
		except:
			print(title + 'Histogram Plotting Position Failed')
			return 
	if not reverse_axis:
		ax.hist(values,width = w,histtype='bar',bins=binnum,color=Color,edgecolor='none') 
		ax.set_xlabel(Xlabel)
		ax.set_ylabel(Ylabel)
		ax.set_title(title)
		if upperlimit:
			ax.set_ylim([0 ,upperlimit])
		if tx and ty:
			lw = 1
			ax.axvline(np.average(values), color='red', linestyle='dashed', linewidth=lw)
			ax.axvline(np.average(values)+np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axvline(np.average(values)-np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axvline(np.average(values)+2*np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axvline(np.average(values)-2*np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axvline(np.average(values)+3*np.std(values), color='#FF0000', linestyle='solid', linewidth=lw,alpha = 0.7)
			ax.axvline(np.average(values)-3*np.std(values), color='#FF0000', linestyle='solid', linewidth=lw,alpha = 0.7)
			ax.text(tx,ty,"mean:%f\nstandard deviation:%f"%(np.average(values),np.std(values)))
	else:
		ax.hist(values,height = w,histtype='bar',bins=binnum,color=Color,edgecolor='none',orientation='horizontal')
		ax.set_ylabel(Xlabel)
		ax.set_xlabel(Ylabel)
		ax.set_title(title)
		if upperlimit:
			ax.set_xlim([0 ,upperlimit])
		if tx and ty:
			lw = 1
			ax.axhline(np.average(values), color='red', linestyle='dashed', linewidth=lw)
			ax.axhline(np.average(values)+np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axhline(np.average(values)-np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axhline(np.average(values)+2*np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axhline(np.average(values)-2*np.std(values), color='#225522', linestyle='dashed', linewidth=lw,alpha = 0.7)
			ax.axhline(np.average(values)+3*np.std(values), color='#FF0000', linestyle='solid', linewidth=lw,alpha = 0.7)
			ax.axhline(np.average(values)-3*np.std(values), color='#FF0000', linestyle='solid', linewidth=lw,alpha = 0.7)
			ax.text(ty,tx,"mean:%f\nstandard deviation:%f"%(np.average(values),np.std(values)))


		
def subplt2dScatters(Fig,pos,xl,yl,values,title):
	ax = fig.add_subplot(pos)
	ax.scatter(xl,yl,c = values,cmap = cm.jet,s=30,marker='s',edgecolors=None,lw=0)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_title(title)
	
def subpltColorAxes(Fig,bar,values):
	cax = Fig.add_axes(bar)
	norm = mpl.colors.Normalize(vmin=min(values), vmax=max(values))
	cb = mpl.colorbar.ColorbarBase(cax, cmap=cm.jet, norm=norm, spacing='proportional')

def subpltCorr(Fig,pos,xvalues,yvalues,title,Xlabel='IDDQ',Ylabel='Delta IDDQ',tx=False,ty=False,showStd=False):
	xavg=np.average(xvalues)
	xstd=np.std(xvalues)
	yavg=np.average(yvalues)
	ystd=np.std(yvalues)
	ax = Fig.add_subplot(pos)
	ax.scatter(xvalues,yvalues,s=10,marker='s',alpha=0.5)
	ax.axvline(xavg,color='red',linestyle='dashed',linewidth=1)
	ax.axhline(yavg,color='red',linestyle='dashed',linewidth=1)
	if showStd:
		ax.axvline(xavg-3*xstd,color='red',linestyle='solid',linewidth=1)
		ax.axvline(xavg+3*xstd,color='red',linestyle='solid',linewidth=1)
		ax.axhline(yavg-3*ystd,color='red',linestyle='solid',linewidth=1)
		ax.axhline(yavg+3*ystd,color='red',linestyle='solid',linewidth=1)
	ax.set_xlabel(Xlabel)
	ax.set_ylabel(Ylabel)
	ax.set_title(title)
	if tx and ty:
		ax.text(tx,ty,"Correlation Coefficient:%f"%np.corrcoef(xvalues,yvalues)[0][1])

def subpltPlot(Fig,pos,values,title,Xlabel='Patterns',Ylabel='IDDQ',tx=False,ty=False):
	ax = Fig.add_subplot(pos)
	ax.ticklabel_format(useOffset=False) # Not using offset
	axx = np.array([i+1 for i in range(len(values))])
	ax.plot(axx,values)
	ax.scatter(axx,values)
	ax.set_title(title)
	ax.set_xlabel(Xlabel)
	ax.set_ylabel(Ylabel)
	ax.set_ylim([np.average(values)-5 ,np.average(values)+5])
	
	
#####################################################################
#####################################################################

def tripleCorrelation(Fig,IList,DList,title=None,index=None):
	if title:
		if index != None :
			Fig.suptitle(title+"|Iterative Round %d"%index)
		else:
			Fig.suptitle(title)
	elif index != None:
		Fig.suptitle("Iterative Round %d"%(index))
	subpltCorr(Fig,223,IList,DList,'',Xlabel='Maximum IDDQ',Ylabel='Maximum Delta IDDQ',tx=65,ty=5,showStd=True)
	subpltHist(Fig,221,IList,"Maximum IDDQ",binnum = 60,upperlimit = 100,tx = 40,ty = 50)
	subpltHist(Fig,224,DList,"Maximum Delta IDDQ",binnum=60,upperlimit=20,tx=5,ty=8,reverse_axis=True)
#####################################################################	
#####################################################################
def showFigures(MaxAllList,TestList,IMaxList):
	

	#plotting distribution of patterns

	#figpat = plt.figure()
	#subpltHist(figpat,121,abs(TestList[116]),'116',Xlabel='Delta IDDQ of 116(mA)',binnum = 60,upperlimit = 100,tx = 5,ty = 50)
	#subpltHist(figpat,122,abs(TestList[117]),'117',Xlabel='Delta IDDQ of 117(mA)',binnum = 60,upperlimit = 100,tx = 5,ty = 50)

	#figpat2 = plt.figure()
	#subpltHist(figpat2,121,abs(TestList[240]),'240',Xlabel='Delta IDDQ of 240(mA)',binnum = 60,upperlimit = 100,tx = 2,ty = 50)
	#subpltHist(figpat2,122,abs(TestList[241]),'241',Xlabel='Delta IDDQ of 241(mA)',binnum = 60,upperlimit = 100,tx = 2,ty = 50)
	
	#Plotting corelations between IDDQ and Delta IDDQ
	
	figCor2=plt.figure()
	tripleCorrelation(figCor2,IMaxList,MaxAllList,"Correlation of Maximum IDDQ and Maximum Delta IDDQ")
	
	
	#####################################################################
	#Plotting distribution of deleted dies
	#figdelm = plt.figure()
	#figdelm.suptitle("Distribution of maximum delta IDDQ ")
	#subpltHist(figdelm,131,MaxAllList,'before pattern selection',binnum=40,upperlimit=100,tx=5,ty=70)
	#subpltHist(figdelm,132,MaxAllList_Del_out,'outlier pattern deletion',binnum=60,upperlimit=100,tx=5,ty=70)
	#subpltHist(figdelm,133,MaxAllList_Del,'2 cluster pattern deletion',binnum=60,upperlimit=100,tx=5,ty=70)
	
	#plt.show()
	
	
def saveFigures(IMaxList,MaxAllList,iter_round,fileName,mode=None):
	figCor=plt.figure()
	if mode == None:
		tripleCorrelation(figCor,IMaxList,MaxAllList,"Correlation of Maximum IDDQ and Maximum Delta IDDQ %d"%iter_round)
		figCor.savefig(fileName.strip('.csv')+'_round_%d'%(iter_round),dpi=200)	
	else:
		tripleCorrelation(figCor,IMaxList,MaxAllList,"Correlation of Maximum IDDQ and Maximum Delta IDDQ %d MODE %d"%(iter_round,mode))
		figCor.savefig(fileName.strip('.csv')+'_mode_%d_round_%d'%(mode,iter_round),dpi=200)	

def savePatterns(TestList,fileName=False):
	fig =plt.figure()
	for num_name in TestList:
		num,name = num_name
		try:
			subpltHist(fig,111,TestList[num_name],'%d,%s'%(num,name),Xlabel='IDDQ (mA)',
			binnum = 60,tx = 100,ty = 5)
		except:		
			print(num,end='|')
			print(name)
		#subpltHist(fig,122,abs(TestList[num]),'abs(%d)'%num,Xlabel='Delta IDDQ of %d(mA)'%num,binnum = 60,upperlimit = 100,tx = 0.1,ty = 50)
		if fileName:
			fig.savefig(fileName.strip('.csv')+'_pattern_%s_%d.png'%(name,num),dpi=200)	
		else:
			fig.savefig('%d.png'%(num),dpi=200)	
		fig.clf()



def saveDeltaPatterns(DTestList,Round,NumNames=False,fileName=False):
	fig =plt.figure()
	if not NumNames:
		iter_=DTestList
	else:
		iter_=NumNames
	for il,ir in iter_:
		ilnum,ilname = il
		irnum,irname = ir
		
		iln = ilname.strip('_iddq scan_IDDQ -1')+'_'+str(ilnum)
		irn = irname.strip('_iddq scan_IDDQ -1')+'_'+str(irnum)
		try:
			subpltHist(fig,111,DTestList[(il,ir)],'%s-%s'%(iln,irn),Xlabel='Delta IDDQ (mA)',
			binnum = 60,tx = 0.1,ty = 5)
		except:		
			print(iln,end='-')
			print(irn)
		#subpltHist(fig,122,abs(TestList[num]),'abs(%d)'%num,Xlabel='Delta IDDQ of %d(mA)'%num,binnum = 60,upperlimit = 100,tx = 0.1,ty = 50)
		if fileName:
			fig.savefig(fileName.strip('.csv')+'_delta_%s-%s_round%d.png'%(iln,irn,Round),dpi=200)	
		else:
			fig.savefig('%s-%s.png'%(iln,irn),dpi=200)	
		fig.clf()

def saveModeDies(all_die_list,fileName):
	fig =plt.figure()
	for ID in all_die_list:
		die = all_die_list[ID]
		for mode in die['Mode']:
			if mode == 0 or mode == 3 or mode ==8 :		
				vlist = die[mode]['Value']
				subpltHist(fig,121,vlist,'ID:%d|%d'%(ID,mode),Xlabel='IDDQ (mA)',
				binnum = 60,tx = 0.1,ty = 5)
				subpltPlot(fig,122,vlist,'ID:%d|%d'%(ID,mode),Xlabel='Patterns',Ylabel='IDDQ')
				fig.savefig(fileName.strip('.csv')+'_mode%d_die%d.png'%(mode,ID),dpi=200)
				fig.clf()
		

def observeMode8Dies(all_die_list,fileName):
	fig =plt.figure()
	
	ax = fig.add_subplot(111)
	ax.ticklabel_format(useOffset=False) # Not using offset
	ax.set_title('mode8_dies')
	ax.set_xlabel('Patterns')
	ax.set_ylabel('IDDQ(mA)')
	
	fig2 =plt.figure()
	ax2 = fig2.add_subplot(111)
	ax2.ticklabel_format(useOffset=False) # Not using offset
	ax2.set_title('mode8_strange_dies')
	ax2.set_xlabel('Patterns')
	ax2.set_ylabel('IDDQ(mA)')
	
	
	pool =[60,151,120,38]
	for ID in all_die_list:
		die = all_die_list[ID]
		for mode in die['Mode']:
			if mode ==8 :		
				values = die[mode]['Value']
				axx = np.array([i+1 for i in range(len(values))])
				ax.plot(axx,values)
				#ax.scatter(axx,values)
				'''try:
					if values[7]>values[8] or values[12]>values[13] or ID in pool:
						print("shiftL ID:%d|%f"%(ID,np.average(values)))
						ax2.plot(axx,values)
						ax2.scatter(axx,values)
					elif values[9]>values[8] or values[14]>values[13]:
						print("shiftR ID:%d"%ID)
						ax2.plot(axx,values)
						ax2.scatter(axx,values)
				except:
					print("too short ID:%d"%ID)'''
	
	fig.savefig(fileName.strip('.csv')+'_mode8_observation.png',dpi=200)
	fig2.savefig(fileName.strip('.csv')+'_mode8_observation_strange.png',dpi=200)
	#fig.clf()
	
	
	
	
	
	#ax.set_ylim([np.average(values)-5 ,np.average(values)+5])

#def saveChosenPatterns(TestList,NumNames,fileName):
#	fig =plt.figure()
#	for num_name in NumNames:
#		num,name = num_name
#		subpltHist(fig,121,TestList[num_name],'%d,%s'%(num,name),Xlabel='Delta IDDQ of %d,%s(mA)'%(num,name),
#		binnum = 60,upperlimit = 100,tx = 0.1,ty = 50)
#		subpltHist(fig,122,abs(TestList[num_name]),'abs(%d,%s)'%(num,name),Xlabel='Delta IDDQ of %d,%s(mA)'%(num,name),
#		binnum = 60,upperlimit = 100,tx = 0.1,ty = 50)
#		fig.savefig(fileName.strip('.csv')+'_delta%d.png'%(num),dpi=200)	
#		fig.clf()

#def saveChosenIddqPatterns(TestList,Nums,fileName):
#	fig =plt.figure()
#	for num in Nums:
#		subpltHist(fig,111,TestList[num],'%d'%num,Xlabel='IDDQ of %d(mA)'%num,binnum = 60,tx = 75,ty = 50)
#		#subpltHist(fig,122,abs(TestList[num]),'abs(%d)'%num,Xlabel='Delta IDDQ of %d(mA)'%num,binnum = 60,upperlimit = 100,tx = 0.1,ty = 50)
#		fig.savefig(fileName.strip('.csv')+'_pattern%d.png'%(num),dpi=200)	
#		fig.clf()


#def saveIDDQ(iddqvlist,infileName,mode):
#	fig = plt.figure()
#	title = infileName.strip('.txt')+'_mode%d'%mode
#	subpltPlot(fig,111,iddqvlist,title,Xlabel='IDDQ Patterns',Ylabel='IDDQ(mA)',tx=False,ty=False)
#	fig.savefig(title+'.png',dpi=fig.dpi)

#def saveIDDQ2(iddqvlist,title):
#	fig = plt.figure()
#	subpltPlot(fig,111,iddqvlist,title,Xlabel='IDDQ Patterns',Ylabel='IDDQ(mA)',tx=False,ty=False)
#	fig.savefig(title+'.png',dpi=fig.dpi)

	

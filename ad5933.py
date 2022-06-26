from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from guiFunctions import *
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import serial
import math
import time
from scipy.optimize import curve_fit




plot_freq=0
plot_inc_val=0
plot_no_inc=0

s  = 0
comportval = 0
#serial_data = 0 #for serial data plotting from text file


def setcomport():
	global s,comportval
	comportval = str(comport.get())
	s = serial.Serial(comportval,baudrate=9600,timeout=0.01)
	Label(root,text="			            ",bg='#9EE9FD').place(relx=1,rely=0.95,anchor='se')
	Label(root,text="   Comport Connected   ").place(relx=1,rely=0.95,anchor='se')

def close_comport():
	global s
	s.close()
	Label(root,text="			           ",bg='#9EE9FD').place(relx=1,rely=0.95,anchor='se')
	Label(root,text=" Comport Disconnected ").place(relx=1,rely=0.95,anchor='se')

reg_0x80=0
reg_0x80_v=0
reg_0x80_g=0
reg_0x81=0

reg_0x82=0
reg_0x83=0
reg_0x84=0
reg_0x85=0
reg_0x86=0
reg_0x87=0
reg_0x88=0
reg_0x89=0

reg_0x8A=0
reg_0x8A_st=0
reg_0x8A_st_m=0
reg_0x8B=0

reg_0x8F=0

reg_0x94=0
reg_0x95=0
reg_0x96=0
reg_0x97=0

increments = 0#-------------------------------
# data = 10



# variables for Gain
magnitude = 0
phase = 0
gain = 0
Rfb_resistance = 0





def popup_freq():
	messagebox.showinfo("Start Frequency","Put value in box and set Ok. The Frequency range for Transmit stage is 1-100 kHz")

def popup_inc_freq():
	messagebox.showinfo("Frequency Increment","Choose the Step Size of Frequency")

def popup_no_of_inc():
	messagebox.showinfo("Number of Increments","Max number of Increments is 511")

def popup_settling_time():
	messagebox.showinfo("Settling Time","Set the maximum amount of time for DDS Conversion, First select Settling time multiplier")

def popup_comport_select():
	messagebox.showinfo("Comport Selection","Enter the COM port to which Arduino is attached, e.g. \"COM3\"")





def open_cal():
	xy=10
def short_cal():
	xy=10
def load_cal():
	xy=10

def open_cal_popup():
	messagebox.showinfo("Open Calibration","Let the terminals(Vin and Vout) of the device OPEN and click open button and wait for 10 seconds, it will automatically do OPEN callibration")

def short_cal_popup():
	messagebox.showinfo("Short Calibration","Let the terminals(Vin and Vout) of the device SHORT and click Short button and wait for 10 seconds, it will automatically do SHORT callibration")

def load_cal_popup():
	messagebox.showinfo("Load Calibration","Put a 50 ohm Load in between the terminals of the device and click load button and wait for 10 seconds, it will automatically do LOAD callibration")









def set_Rfb_value():
	global Rfb_resistance
	Rfb_resistance = int(res_val_gain.get())

def Rfb_value_popup():
	messagebox.showinfo("Feedback Resistance","Input the value of feedback resistance which is between Rfb and Vin pins of AD5933")


def set_gain_val():
	global Rfb_resistance,gain,phase
	s.write("8".encode())
	time.sleep(0.2)
	for i in range(100):
		if (s.in_waiting): #or only s.in_waiting:
			data = s.readline().decode('utf').rstrip('\n')
			time.sleep(0.2)
			print(data)
			Label(frame11,text=data).grid(row=2,column=0,padx=5,pady=5)

def set_gain_val_popup():
	messagebox.showinfo("Gain Calculation","Put a Gain Setting Resistor in between Rfb and Vin pins of AD5933 and click this button to get value of magnitude and phase for Gain and system phase calculation")







def freq_val():
	# global A,B,C,plot_freq			#------------------------------------------------------------------------------------------------------------------------------------ It was previously set
	global reg_0x82,reg_0x83,reg_0x84,plot_freq
	frequecny = int(freq.get()) #/4194000*2^27 or *134217728
	plot_freq = frequecny
	if frequecny == 1:
		frequecny = int((frequecny/4194000)*134217728)+1
	else:
		frequecny = int((frequecny/4194000)*134217728)
	start_freq_req_1 = get_reg_1(frequecny)
	start_freq_req_2 = get_reg_2(frequecny)
	start_freq_req_3 = get_reg_3(frequecny)
	Label(frame9,text="			      ").grid(row=0,column=0)
	Label(frame9,text="frequecny values: " + str(start_freq_req_1) +"   " +str(start_freq_req_2)+"   "+str(start_freq_req_3)).grid(row=0,column=0)
	#Label(root,text=frequecny).grid(row=0,column=6)
	reg_0x82 = str(start_freq_req_1)
	reg_0x83 = str(start_freq_req_2)
	reg_0x84 = str(start_freq_req_3)
	s.write("1".encode())
	time.sleep(0.2)
	s.write(reg_0x82.encode())
	time.sleep(0.2)
	s.write(reg_0x83.encode())
	time.sleep(0.2)
	s.write(reg_0x84.encode())

def inc_freq_val():
	global reg_0x85,reg_0x86,reg_0x87,plot_inc_val
	freq_increment = int(inc_freq.get())
	plot_inc_val = freq_increment
	if freq_increment == 1:
		freq_increment = int((freq_increment/4194000)*134217728)+1
	else:
		freq_increment = int((freq_increment/4194000)*134217728)
	inc_freq_reg_1 = get_reg_1(freq_increment)
	inc_freq_reg_2 = get_reg_2(freq_increment)
	inc_freq_reg_3 = get_reg_3(freq_increment)
	Label(frame9,text="			      ").grid(row=1,column=0)
	Label(frame9,text="Increment values : "+str(inc_freq_reg_1)+"   "+str(inc_freq_reg_2)+"   "+str(inc_freq_reg_3)).grid(row=1,column=0)
	#Label(root,text=freq_increment).grid(row=1,column=6)
	reg_0x85 = str(inc_freq_reg_1)
	reg_0x86 = str(inc_freq_reg_2)
	reg_0x87 = str(inc_freq_reg_3)
	s.write("2".encode())
	time.sleep(0.2)
	s.write(reg_0x85.encode())
	time.sleep(0.2)
	s.write(reg_0x86.encode())
	time.sleep(0.2)
	s.write(reg_0x87.encode())

def no_of_inc_val():
	global reg_0x88,reg_0x89,increments,plot_no_inc #------------------incrementes new
	increments = int(no_of_inc.get())
	plot_no_inc = increments
	no_of_inc_reg_1 = get_reg_2(increments)
	no_of_inc_reg_2 = get_reg_3(increments)
	Label(frame9,text="			      ").grid(row=2,column=0)
	Label(frame9,text="no of increments : "+str(no_of_inc_reg_1)+"   "+str(no_of_inc_reg_2)).grid(row=2,column=0)
	#Label(root,text=increments).grid(row=2,column=6)
	reg_0x88 = str(no_of_inc_reg_1)
	reg_0x89 = str(no_of_inc_reg_2)
	s.write("3".encode())
	time.sleep(0.2)
	s.write(reg_0x88.encode())
	time.sleep(0.2)
	s.write(reg_0x89.encode())


def settling_time_val():
	global reg_0x8A,reg_0x8A_st,reg_0x8B
	set_time = int(settling_time.get())
	set_time_reg_1 = get_reg_2(set_time)
	set_time_reg_2 = get_reg_3(set_time)
	#Label(root,text=str(set_time_reg_1)+"   "+str(set_time_reg_2)).grid(row=3,column=3)
	#Label(root,text=set_time).grid(row=3,column=6)
	reg_0x8A_st = set_time_reg_1
	reg_0x8B = str(set_time_reg_2)
	reg_0x8A = str(reg_0x8A_st + reg_0x8A_st_m)
	Label(frame9,text="			      ").grid(row=3,column=0)
	Label(frame9,text="Setttling time : "+str(reg_0x8A)+"   "+str(reg_0x8B)).grid(row=3,column=0)
	s.write("4".encode())
	time.sleep(0.2)
	s.write(reg_0x8A.encode())
	time.sleep(0.2)
	s.write(reg_0x8B.encode())

def setreg81val():
	reg81val = str(reg_0x81)
	Label(frame9,text="			      ").grid(row=4,column=0)
	Label(frame9,text="reg 81 : "+str(reg_0x81)).grid(row=4,column=0)
	s.write("5".encode())
	time.sleep(0.2)
	s.write(reg81val.encode())
	time.sleep(0.2)

def setreg80val():
	global reg_0x80,reg_0x80_v,reg_0x80_g
	reg_0x80 = str(reg_0x80_v + reg_0x80_g)
	Label(frame9,text="			      ").grid(row=5,column=0)
	Label(frame9,text="reg 80 : "+str(reg_0x80_v)+"   "+str(reg_0x80_g)+"	  "+reg_0x80).grid(row=5,column=0)
	s.write("6".encode())
	time.sleep(0.2)
	s.write(reg_0x80.encode())
	time.sleep(0.2)

def start_sweep():
	s.write("7".encode())
	time.sleep(0.2)
	file = open('serialdata.txt','w')
	forloopval = 3*increments
	for i in range(forloopval):
		if (s.in_waiting): #or only s.in_waiting:
			data = s.readline().decode('utf').rstrip('\n')
			time.sleep(0.2)
			print(data)
			file.write(data)
		#time.sleep(0.05)
	file.close()
	Label(root,text=" Impedance Spectroscopy Complete    ").place(relx=0.5,rely=0.5,anchor='center')
	# while True:
	# 	if s.in_waiting: #or only s.in_waiting:
	# 		data = s.readline().decode('utf').rstrip('\n')
	# 		print(data)
	# 		time.sleep(0.2)


def voltage_clicked(value):
	global reg_0x80_v
	reg_0x80_v = value
	Label(frame9,text="			      ").grid(row=6,column=0)
	Label(frame9,text="reg_80_v : "+str(value)).grid(row=6,column=0)
def gain_clicked(value):
	global reg_0x80_g
	reg_0x80_g = value
	Label(frame9,text="			      ").grid(row=7,column=0)
	Label(frame9,text="reg_80_g : "+str(value)).grid(row=7,column=0)
def clock_clicked(value):
	global reg_0x81
	reg_0x81 = value
	Label(frame9,text="			      ").grid(row=8,column=0)
	Label(frame9,text="reg_81 : "+str(value)).grid(row=8,column=0)
def st_clicked(value):
	global reg_0x8A_st_m
	reg_0x8A_st_m = value
	Label(frame9,text="			      ").grid(row=9,column=0)
	Label(frame9,text="reg_8A_st_m : "+str(value)).grid(row=9,column=0)



#def func(): #just for checking
#	texty = "hello" + freq.get()
#	Label(root,text=texty).grid(row=0,column=3)

root = Tk()	
root.title('Impedance Spectroscopy Software')
# root.iconbitmap('C:/Users/Tayyab/Desktop/gui/gui6icon1.ico')
root.geometry("1250x650")
root.configure(bg='#9EE9FD')
# root.configure(bg='#8FB9A8')
# root.configure(bg='#344E5C')
# root.configure(bg='#353C45')






seriesRC     =  ImageTk.PhotoImage(Image.open("seriesRC.png"))
seriesRL     =  ImageTk.PhotoImage(Image.open("seriesRL.png"))
seriesRLC    =  ImageTk.PhotoImage(Image.open("seriesRLC.png"))
parallelRC   =  ImageTk.PhotoImage(Image.open("parallelRC.png"))
parallelRL   =  ImageTk.PhotoImage(Image.open("parallelRL.png"))
parallelRLC  =  ImageTk.PhotoImage(Image.open("parallelRLC.png"))
combination  =  ImageTk.PhotoImage(Image.open("combination.png"))

#Label(root,text="").grid(row=0,column=0)

frame0 = LabelFrame(root, text="Select ComPort", padx=5,pady=5,bg='#6769FF')
frame0.grid(row=0,column=0,padx=20,pady=10)	

comport = Entry(frame0)
comport.grid(row=0,column=0,padx=20,pady=10)
Button(frame0,text="Set COMport",command=setcomport).grid(row=0,column=1,padx=10,pady=0)
Button(frame0,text="info",command=popup_comport_select).grid(row=0,column=2,padx=10,pady=0)


frame1 = LabelFrame(root, text="Input Parameters", padx=5,pady=5,bg='#6769FF')
frame1.grid(row=1,column=0,padx=20,pady=10)#inside padding , can also remove text for a box only
#outside padding

freq_label = Label(frame1,text="Start Frequency(Hz)").grid(row=0,column=0,padx=10,pady=10)
inc_freq_label = Label(frame1,text="Increment size").grid(row=1,column=0,padx=0,pady=0)
no_of_inc_label = Label(frame1,text="Number of Increments").grid(row=2,column=0,padx=0,pady=0)

freq = Entry(frame1)
freq.grid(row=0,column=1,padx=20,pady=10)
inc_freq = Entry(frame1)
inc_freq.grid(row=1,column=1,padx=0,pady=10)
no_of_inc = Entry(frame1)
no_of_inc.grid(row=2,column=1,padx=0,pady=10)
no_of_inc.insert(0,"max value 511")


Button(frame1,text="Set value",command=freq_val).grid(row=0,column=2,padx=10,pady=0)
Button(frame1,text="Set value",command=inc_freq_val).grid(row=1,column=2,padx=10,pady=0)
Button(frame1,text="Set value",command=no_of_inc_val).grid(row=2,column=2,padx=10,pady=0)


Button(frame1,text="info",command=popup_freq).grid(row=0,column=3,padx=10,pady=0)
Button(frame1,text="info",command=popup_inc_freq).grid(row=1,column=3,padx=10,pady=0)
Button(frame1,text="info",command=popup_no_of_inc).grid(row=2,column=3,padx=10,pady=0)


#messagebox.showinfo("This is title", "Actual popup").grid(row=0,column=2,padx=5,pady=0)



#freq.insert(0,"Enter Start Freq(Hz)") 



v = IntVar()
c = IntVar()
g = IntVar()
st = IntVar()

v.set(0)
c.set(0)
g.set(1)
st.set(0)



frame7 = LabelFrame(root, text="Output Excitation Voltage & Programmable Gain", padx=5,pady=5,bg='#6769FF')
frame7.grid(row=3,column=0,padx=10,pady=10)
frame2 = LabelFrame(frame7, text="Output Excitation Voltage", padx=5,pady=5)
frame2.grid(row=0,column=0,padx=10,pady=10)
Radiobutton(frame2, text='2.0v p-p', variable=v,value=0,command=lambda: voltage_clicked(v.get())).pack()
Radiobutton(frame2, text='1.0v p-p', variable=v,value=6,command=lambda: voltage_clicked(v.get())).pack()
Radiobutton(frame2, text='0.4v p-p', variable=v,value=4,command=lambda: voltage_clicked(v.get())).pack()
Radiobutton(frame2, text='0.2v p-p', variable=v,value=2,command=lambda: voltage_clicked(v.get())).pack()
frame4 = LabelFrame(frame7, text="Programmable Gain", padx=5,pady=5)
frame4.grid(row=0,column=1,padx=10,pady=10)
Radiobutton(frame4, text='x1', variable=g,value=1,command=lambda: gain_clicked(g.get())).pack()
Radiobutton(frame4, text='x5', variable=g,value=0,command=lambda: gain_clicked(g.get())).pack()
Button(frame7,text="Set value",command=setreg80val).grid(row=0,column=2,padx=10,pady=10)


frame3 = LabelFrame(root, text="System Clock", padx=5,pady=5,bg='#6769FF')
frame3.grid(row=0,column=1,padx=10,pady=10)
Radiobutton(frame3, text='External', variable=c,value=8,bg='#6769FF',command=lambda: clock_clicked(c.get())).pack()
Radiobutton(frame3, text='Internal', variable=c,value=0,bg='#6769FF',command=lambda: clock_clicked(c.get())).pack()
Button(frame3,text="Set value",command=setreg81val).pack()


frame6 = LabelFrame(root, text="Setling Time cycles", padx=5,pady=5,bg='#6769FF')
frame6.grid(row=2,column=0,padx=10,pady=10)
settling_time_label = Label(frame6,text="Settling Time").grid(row=0,column=0,padx=10,pady=0)
settling_time = Entry(frame6)
settling_time.grid(row=0,column=1,padx=0,pady=10)
settling_time.insert(0,"max value 511")
Button(frame6,text="Set value",command=settling_time_val).grid(row=1,column=2,padx=10,pady=0)
Button(frame6,text="info",command=popup_settling_time).grid(row=1,column=3,padx=10,pady=0)
frame5 = LabelFrame(frame6, text="Setling Time Multiplier", padx=5,pady=5)
frame5.grid(row=1,column=1,padx=10,pady=10)
Radiobutton(frame5, text='x1 (Default)', variable=st,value=0,command=lambda: st_clicked(st.get())).grid(row=0,column=0,padx=10,pady=0)
Radiobutton(frame5, text='x2 (Double)', variable=st,value=2,command=lambda: st_clicked(st.get())).grid(row=1,column=0,padx=10,pady=0)
Radiobutton(frame5, text='x4 (Quadruple)', variable=st,value=6,command=lambda: st_clicked(st.get())).grid(row=2,column=0,padx=10,pady=0)


frame8 = LabelFrame(root, text="Start Sweep", padx=5,pady=5,bg='#6769FF')
frame8.grid(row=0,column=2,padx=10,pady=10)
Button(frame8,text="Start Sweep",command=start_sweep).pack()

Button(root,text="close comport",command=close_comport).place(rely=1,relx=1,anchor='se')


program_label = Label(root,text="Impdance Analysis: Device AD5933",font=("calibri body",10)).place(relx=0.5,rely=1,anchor='s')


# -------------------------------------------------------------------------------------------

def graph_plot():
	global plot_freq,plot_no_inc,plot_inc_val
	Label(root,text=" 								    ",bg='#9EE9FD').place(relx=0.5,rely=0.5,anchor='center')

	imp_data = []
	phs_data = []
	x_axis   = []

	y_start=[]
	y_end=[]

	serial_data=np.loadtxt("serialdata.txt",dtype='str',delimiter=",")
	imp_data0 = serial_data[:,1] #read all rows of first index column
	phs_data0 = serial_data[:,2]

	stop_val = plot_freq+ plot_no_inc*plot_inc_val +1	
	x_axis0 = np.arange(plot_freq,stop_val,plot_inc_val)	

	for i in range(len(imp_data0)):
		imp_data.append(float(imp_data0[i]))

	for i in range(len(phs_data0)):
		phs_data.append(float(phs_data0[i]))

	for i in range(len(x_axis0)):
		x_axis.append(x_axis0[i])

	x_start = plot_freq;
	x_end = x_axis[len(x_axis)-1]

	print(x_axis)
	print(imp_data)
	print(phs_data)


	if (imp_data[0]>=1000 and imp_data[0]<=10000):
		y_start.append(float(imp_data[0]-5000))
		y_end.append(float(imp_data[len(imp_data)-1]+5000))
		print(y_end)
	elif (imp_data[0]>=10000 and imp_data[0]<=100000):
		y_start.append(float(imp_data[0]-50000))
		y_end.append(float(imp_data[len(imp_data)-1]+50000))
		print(y_end)
	elif (imp_data[0]>=100000 and imp_data[0]<=1000000):
		y_start.append(float(imp_data[0]-500000))
		y_end.append(float(imp_data[len(imp_data)-1]+500000))
		print(y_end)
	elif (imp_data[0]>=1000000 and imp_data[0]<=10000000):
		y_start.append(float(imp_data[0]-5000000))
		y_end.append(float(imp_data[len(imp_data)-1]+5000000))
		print(y_end)
	elif (imp_data[0]>=10000000 and imp_data[0]<=100000000):
		y_start.append(float(imp_data[0]-50000000))
		y_end.append(float(imp_data[len(imp_data)-1]+50000000))
		print(y_end)


	plt.figure()
	plt.subplot(1,2,1)
	#plt.axis([plot_freq+1000,x_axis[len(x_axis)-1]+1000,imp_data[0]-5000000,imp_data[len(imp_data)-1]+5000000])
	#plt.axis([plot_freq,x_axis[len(x_axis)-1],imp_data[0]-5000000,imp_data[len(imp_data)-1]+5000000])
	plt.axis([x_start,x_end,y_start[0],y_end[0]])
	plt.plot(x_axis,imp_data)
	plt.title("Impedance")
	plt.xlabel("Frequency")
	plt.ylabel("Impedance")
	
	plt.subplot(1,2,2)
	plt.axis([plot_freq,x_axis[len(x_axis)-1],phs_data[0]-180,phs_data[len(imp_data)-1]+180])
	plt.plot(x_axis,phs_data)
	plt.title("phase")
	plt.xlabel("Frequency")
	plt.ylabel("Phase")
	plt.suptitle("Impedance Spectroscopy")
	plt.show()

	# plt.plot(x_axis,imp_data)
	# plt.show()
	# plt.plot(x_axis,phs_data)
	# plt.show()
	print(x_axis)
	print(imp_data)
	print(phs_data)

#----------------------------------------------------------------------------------------------------

Button(root,text="Graph",command=graph_plot).grid(row=0,column=8)

frame9 = LabelFrame(root, text="Values", padx=5,pady=5,bg='#6769FF')
frame9.place(relx=1,rely=0,anchor='ne')


frame10 = LabelFrame(root, text="Calibration", padx=5,pady=5,bg='#6769FF')
frame10.grid(row=0,column=3)

Button(frame10,text="Open",command=open_cal).grid(row=0,column=0)
Button(frame10,text="Short",command=short_cal).grid(row=1,column=0)
Button(frame10,text="Load",command=load_cal).grid(row=2,column=0,padx=10,pady=5)

Button(frame10,text="info",command=open_cal_popup).grid(row=0,column=1,padx=10,pady=5)
Button(frame10,text="info",command=short_cal_popup).grid(row=1,column=1)
Button(frame10,text="info",command=load_cal_popup).grid(row=2,column=1)


frame11 = LabelFrame(root,text="Gain Value",padx=5,pady=5,bg='#6769FF')
frame11.grid(row=1,column=1)

Label(frame11,text="Rfb Value").grid(row=0,column=0,padx=5,pady=5)
res_val_gain = Entry(frame11)
res_val_gain.grid(row=0,column=1,padx=5,pady=5)
Button(frame11,text="Set",command=set_Rfb_value).grid(row=0,column=2,padx=5,pady=5)
Button(frame11,text="info",command=Rfb_value_popup).grid(row=0,column=3,padx=5,pady=5)

Label(frame11,text="Gain").grid(row=1,column=0,padx=5,pady=5)
Button(frame11,text="Get Value",command=set_gain_val).grid(row=1,column=1,padx=5)
Button(frame11,text="Show",command=set_gain_val).grid(row=1,column=2,padx=5)
Button(frame11,text="info",command=set_gain_val_popup).grid(row=1,column=3,padx=5,pady=5)

#------------------------------------------------------------------------------------------------------

frame12 = LabelFrame(root, text="Equivalent Circuit Model", padx=5,pady=5,bg='#6769FF')
frame12.grid(row=1,column=2,padx=5,pady=5)

eqmodel = IntVar()

def equivalentmodelfunction(value):
	global plot_freq,plot_no_inc,plot_inc_val
	x_axis   = []
	imp_data = []

	serial_data=np.loadtxt("serialdata.txt",dtype='str',delimiter=",")

	imp_data0 = serial_data[:,1]
	stop_val = plot_freq+ plot_no_inc*plot_inc_val +1
	x_axis0 = np.arange(plot_freq,stop_val,plot_inc_val)

	for i in range(len(imp_data0)):
		imp_data.append(float(imp_data0[i]))

	for i in range(len(x_axis0)):
		x_axis.append(x_axis0[i])

	print(imp_data0)
	print(imp_data)
	print("  ")
	print(x_axis0)
	print(x_axis)

	imp_data_np = np.array(imp_data)
	x_axis_np = np.array(x_axis)




	if value == 1:
		nw = Toplevel()
		nw.title('RC Equivalent Model')
		Label(nw,image=seriesRC).pack()
		#without scaling
		try:
			def model(x,a,b):										
				return (a**2 + (1/(2*3.14*x*b))**2)**0.5
			
			init_guess = [imp_data_np.min(),1/(imp_data_np.min())]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,c = ans
			print(ans)

			def showModel():
					Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="C = " + str(abs(c)) + ' F' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b):										#a=r , b=c , x=f
				return (a**2 + (1/(2*3.14*x*b))**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,c = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="C = " + str(abs(c)) + ' F' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()




	elif value == 2:
		nw = Toplevel()
		nw.title('RL Equivalent Model')
		Label(nw,image=seriesRL).pack()

		try:
			def model(x,a,b):										#a=r , b=L , x=f
				return (a**2 + (2*3.14*x*b)**2)**0.5
			
			init_guess = [1,1]#---------------------------------------------------------------------------
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,l = ans
			print(ans)

			def showModel():
					Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="L = " + str(abs(l)) + ' H' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for L)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b):										#a=r , b=L , x=f
				return (a**2 + (2*3.14*x*b)**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,l = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="L = " + str(abs(l)) + ' H' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for L)",bg='#facd12').pack()

			showModel()




	elif value == 3:
		nw = Toplevel()
		nw.title('RLC Equivalent Model')
		Label(nw,image=seriesRLC).pack()

		try:
			def model(x,a,b,c):									#a=r , b=L , c=c , x=f
				return (a**2 + ((1/(2*3.14*x*c))-(2*3.14*x*b))**2)**0.5
			
			init_guess = [1,1,1]#---------------------------------------------------------------------------
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,l,c = ans
			print(ans)

			def showModel():
					Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="L = " + str(abs(l)) + ' H' +  '    (without scaling)',bg='#facd12').pack()
					Label(nw,text="C = " + str(abs(l)) + ' F' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for L)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b,c):									#a=r , b=L , c=c , x=f
				return (a**2 + ((1/(2*3.14*x*c))-(2*3.14*x*b))**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,l,c = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="L = " + str(abs(l)) + ' H' +  '    (with scaling)',bg='#facd12').pack()
				Label(nw,text="C = " + str(abs(l)) + ' F' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for L)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()


	elif value == 4:
		nw = Toplevel()
		nw.title('RC Equivalent Model')
		Label(nw,image=parallelRC).pack()

		try:
			def model(x,a,b):										#a=r , b=c , x=f		
				return ((a/(1+a**2*39.4384*x**2*b**2))**2+((a**2*2*3.14*x*b)/(1+a**2*39.4384*x**2*b**2))**2)**0.5
			
			init_guess = [1,1]#---------------------------------------------------------------------------
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,c = ans
			print(ans)

			def showModel():
					Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="C = " + str(abs(c)) + ' F' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b):										#a=r , b=c , x=f		
				return ((a/(1+a**2*39.4384*x**2*b**2))**2+((a**2*2*3.14*x*b)/(1+a**2*39.4384*x**2*b**2))**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,c = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="C = " + str(abs(c)) + ' F' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()


	elif value == 5:
		nw = Toplevel()
		nw.title('RL Equivalent Model')
		Label(nw,image=parallelRL).pack()

		try:
			def model(x,a,b):										#a=r , b=L , x=f		
				return (((a*39.4384*x**2*b**2)/(a**2+39.4984*x**2*b**2))**2+((a**2*2*3.14*x*b)/(a**2+39.4984*x**2*b**2))**2)**0.5
			
			init_guess = [1,1]#---------------------------------------------------------------------------
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,c = ans
			print(ans)

			def showModel():
					Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="L = " + str(abs(c)) + ' H' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for L)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b):										#a=r , b=L , x=f		
				return (((a*39.4384*x**2*b**2)/(a**2+39.4984*x**2*b**2))**2+((a**2*2*3.14*x*b)/(a**2+39.4984*x**2*b**2))**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,c = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="L = " + str(abs(c)) + ' H' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for L)",bg='#facd12').pack()

			showModel()


	elif value == 6:
		nw = Toplevel()
		nw.title('RLC Equivalent Model')
		Label(nw,image=parallelRLC).pack()

		try:
			def model(x,a,b,c):										#a=r , b=L , c=c , x=f		
				return (((a*(b**2/c**2))/((b**2/c**2)+((a*2*3.14*x*b)-(r/(2*3.14*x*c)))**2))**2+((a*(b/c)*((a*2*3.14*x*b)-(r/(2*3.14*x*c))))/((b**2/c**2)+((a*2*3.14*x*b)-(r/(2*3.14*x*c)))**2))**2)**0.5
			
			init_guess = [1,1,1]#---------------------------------------------------------------------------
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,l,c = ans
			print(ans)

			def showModel():
					Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="L = " + str(abs(l)) + ' H' +  '    (without scaling)',bg='#facd12').pack()
					Label(nw,text="C = " + str(abs(l)) + ' F' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for L)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b,c):										#a=r , b=L , c=c , x=f		
				return (((a*(b**2/c**2))/((b**2/c**2)+((a*2*3.14*x*b)-(r/(2*3.14*x*c)))**2))**2+((a*(b/c)*((a*2*3.14*x*b)-(r/(2*3.14*x*c))))/((b**2/c**2)+((a*2*3.14*x*b)-(r/(2*3.14*x*c)))**2))**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r,l,c = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="L = " + str(abs(l)) + ' H' +  '    (with scaling)',bg='#facd12').pack()
				Label(nw,text="C = " + str(abs(l)) + ' F' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for L)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()



	elif value == 7:
		nw = Toplevel()
		nw.title('RLC Equivalent Model')
		Label(nw,image=combination).pack()

		try:
			def model(x,a,b,c):										#a=r1 , b=r2 , c=c , x=f	
				return ((a+(b/(1+b**2*39.4384*x**2*c**2)))**2+((b**2*2*3.14*x*c)/(1+b**2*39.4384*x**2*c**2))**2)**0.5
			
			init_guess = [1,1,1]#---------------------------------------------------------------------------
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r1,r2,c = ans
			print(ans)

			def showModel():
					Label(nw,text="R1 = " + str(abs(r1)) + ' \u03A9' + '    (without scaling)' ,bg='#facd12').pack()
					Label(nw,text="R2 = " + str(abs(r2)) + ' \u03A9' +  '    (without scaling)',bg='#facd12').pack()
					Label(nw,text="C = " + str(abs(c)) + ' F' +  '    (without scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(without scaling couldn't fit the curve for R1)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for R2)",bg='#facd12').pack()
				Label(nw,text="(without scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()

		#then with scaling
		try:
			def model(x,a,b,c):										#a=r1 , b=r2 , c=c , x=f	
				return ((a+(b/(1+b**2*39.4384*x**2*c**2)))**2+((b**2*2*3.14*x*c)/(1+b**2*39.4384*x**2*c**2))**2)**0.5

			if x_axis_np[0]>=1000 and x_axis_np[0]<10000:
				x_axis_np = x_axis_np/1000
			elif x_axis_np[0]>=10000 and x_axis_np[0]<100000:
				x_axis_np = x_axis_np/10000

			if imp_data_np.max()>=1000 and imp_data_np.max()<10000:
				imp_data_np = imp_data_np/1000
			elif imp_data_np.max()>=10000 and imp_data_np.max()<100000:
				imp_data_np = imp_data_np/10000
			elif imp_data_np.max()>=100000 and imp_data_np.max()<1000000:
				imp_data_np = imp_data_np/100000
			elif imp_data_np.max()>=1000000 and imp_data_np.max()<10000000:
				imp_data_np = imp_data_np/1000000

			init_guess = [0.1,0.1]
			fit = curve_fit(model,x_axis_np,imp_data_np,p0=init_guess)
			ans,con = fit
			r1,r2,c = ans
			print(ans)

			def showModel():
				Label(nw,text="R = " + str(abs(r1)) + ' \u03A9' + '    (with scaling)' ,bg='#facd12').pack()
				Label(nw,text="L = " + str(abs(r2)) + ' \u03A9' +  '    (with scaling)',bg='#facd12').pack()
				Label(nw,text="C = " + str(abs(c)) + ' F' +  '    (with scaling)',bg='#facd12').pack()

			showModel()

		except:
			def showModel():
				Label(nw,text="(with scaling couldn't fit the curve for R1)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for R2)",bg='#facd12').pack()
				Label(nw,text="(with scaling couldn't fit the curve for C)",bg='#facd12').pack()

			showModel()





Radiobutton(frame12, text='Series RC',     variable=eqmodel,   value=1).pack()
Radiobutton(frame12, text='Series RL',     variable=eqmodel,   value=2).pack()
Radiobutton(frame12, text='Series RLC',    variable=eqmodel,   value=3).pack()
Radiobutton(frame12, text='Parallel RC',   variable=eqmodel,   value=4).pack()
Radiobutton(frame12, text='Parallel RL',   variable=eqmodel,   value=5).pack()
Radiobutton(frame12, text='Parallel RLC',  variable=eqmodel,   value=6).pack()
Radiobutton(frame12, text='R-R||C',        variable=eqmodel,   value=7).pack()

Button(frame12, text='Calculate Model', command=lambda: equivalentmodelfunction(eqmodel.get())).pack()


#---------------------------------------------------------------------------------------------

root.mainloop()


# fig, axs = plt.subplots(nrows=1,ncols=2,constrained_layout=True)

# axs[0][0].set_title("Impedance")
# axs[0][1].set_title("Phase")

# axs[0][0].plot(x_axis,imp_data)
# axs[0][1].plot(x_axis,phs_data)

# fig.suptitle("Impedance Spectroscopy")

# plt.show()


#logic for control regiter 0x81, (its whole value is zero if internal clock selected) default value of 0x81=00
# 	if system clock = internal check then 0x81= 0
# 	if system clock = external check then 0x81= 8

#logic for control register 0x80,
# 	if gain = 1x then temporary 0x80 = 1 , and if gain = 5x then temporary 0x80=0
# 	if voltage = 2v p-p then temporary 0x80=0 and if voltage = 0.2v p-p 0x80=2 and if voltage = 0.4 p-p 0x80=4 and if voltage = 1v p-p 0x80=6
# 	add these temporary variables to get the value of 0x80 register for the given voltage and gain 

#logic for settling time multiplier
# 	if settling_time set to default then temporary 0x8A=0
# 	if settling-time set to x2 then 	 temporary 0x8A=2
# 	if settling-time set to x4 then      temporary 0x8A=6
# 	add these temporary variable in value of set_time_reg_1 to get full value of 0x8A, and 0x8b will be the set_time_reg_2 value
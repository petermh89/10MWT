from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.simpledialog as tkSimpleDialog
import time
import datetime
import json
import sys
import os

# stopwatch class used from https://www.sourcecodester.com/tutorials/python/11497/python-simple-stopwatch-beginners.html
#everything else that was bunched into this class that isn't clock related is unique
class StopWatch(Frame):  
# Initialize the Main Function of the Stopwatch                                     
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self.startTime = 0.0        
        self.nextTime = 0.0
        self.onRunning = 0
        self.trialOne = 0.0
        self.trialTwo = 0.0
        self.trialThree = 0.0
        self.patient = ""
        self.gait = 0.0
        self.avgGait = StringVar()
        self.timestr = StringVar()
        self.timeOne = StringVar()
        self.timeTwo = StringVar()
        self.timeThree = StringVar()             
        self.MakeWidget()      
 
# Create the widget of the Stopwatch Timer
    def MakeWidget(self):                         
        timeText = Label(self, textvariable=self.timestr, font=("times new roman", 50), fg="green", bg="black")
        self.SetTime(self.nextTime)
        timeText.pack(fill=X, expand=NO, pady=2, padx=2)                      
 
# Continously Update The Time From Counting
    def Updater(self): 
        self.nextTime = time.time() - self.startTime
        self.SetTime(self.nextTime)
        self.timer = self.after(50, self.Updater)
 
# Set The Value of Time When Is Called    
    def SetTime(self, nextElap):
        minutes = int(nextElap/60)
        seconds = int(nextElap - minutes*60.0)
        miliSeconds = int((nextElap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, miliSeconds))
 
# Start The Stopwatch Counting When Button Start Is Clicked        
    def Start(self):                                                     
        if not self.onRunning:            
            self.startTime = time.time() - self.nextTime
            self.Updater()
            self.onRunning = 1        
 
# Stop The Stopwatch Counting When Button Stop Is Clicked
    def Stop(self):                                    
        if self.onRunning:
            self.after_cancel(self.timer)            
            self.nextTime = time.time() - self.startTime    
            self.SetTime(self.nextTime)
            self.onRunning = 0
 
# Close The Application When Exit Button Is Clicked
    def Exit(self):
        result = tkMessageBox.askquestion('10MWT', 'Are you sure you want to exit?', icon='warning')
        if result == 'yes':
            root.destroy()
            exit()
 
# Reset The Timer When Reset Button Is Clicked
    def Reset(self):                                  
        self.startTime = time.time()         
        self.nextTime = 0.0    
        self.SetTime(self.nextTime)
#Restarts app in case new test wants to be started    
    def Restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
#Creates a new patient
    def NewPatient(self):
        self.patient = tkSimpleDialog.askstring("10MWT", "First Name?" )


#Formats time to save in readable format
    def FormatTime(self,currentTime,formType):
        minutes = int(currentTime/60)
        seconds = int(currentTime - minutes*60.0)
        miliSeconds = int((currentTime - minutes*60.0 - seconds)*100)
        Gait = 6.0/self.nextTime

        if (formType == "save"): return str(minutes) + ":" + str(seconds) + ":" + str(miliSeconds)  
        if (formType == "1"): return self.timeOne.set('Time: %02d:%02d:%02d | Gait speed: %.2f m/s' % (minutes, seconds, miliSeconds, Gait))
        if (formType == "2"): return self.timeTwo.set('Time: %02d:%02d:%02d | Gait speed: %.2f m/s' % (minutes, seconds, miliSeconds, Gait))
        if (formType == "3"): return self.timeThree.set('Time: %02d:%02d:%02d | Gait speed: %.2f m/s' % (minutes, seconds, miliSeconds, Gait))

#Saves time and updates display for one of three trials
    def Save(self):
        global avgGait, patient
        if(self.patient == ""): self.NewPatient()
        if (self.trialOne == 0.0):
            self.trialOne = self.FormatTime(self.nextTime,"save")
            self.timeOne = self.FormatTime(self.nextTime,"1")
            avgGait = 6.0/self.nextTime
            self.Reset()
            return

        if (self.trialTwo == 0.0):
            self.trialTwo = self.FormatTime(self.nextTime,"save")
            self.timeTwo = self.FormatTime(self.nextTime,"2")
            avgGait = (avgGait + (6.0/self.nextTime))
            self.Reset()
            return

        if (self.trialThree == 0.0):
            self.trialThree = self.FormatTime(self.nextTime,"save")
            self.timeThree = self.FormatTime(self.nextTime,"3")
            avgGait = (avgGait + (6.0/self.nextTime))/3

            self.avgGait = self.avgGait.set('Avg Gait Speed:  %.2f m/s' % (avgGait))
            self.gait = avgGait
            self.Reset()
            self.DataWriter()

            return

#Writes/creates unique file for patient and stores test data
    def DataWriter(self):
        data = {
            'Name':self.patient,
            'Date': str(datetime.datetime.now()), 
            'Trials':{
                'Trial 1': self.trialOne,
                'Trial 2': self.trialTwo,
                'Trial 3': self.trialThree
                    },
            'Gait Speed': self.gait

            
                }
        dataJSON = json.dumps(data)
        file = str(self.patient).lower() + '.txt'
        with open(file, 'a') as outfile:
            json.dump(dataJSON, outfile)

#Reads txt file and displays past test data
    def DataReader(self):
        patient = tkSimpleDialog.askstring("10MWT", "Which patient record would you like to pull?" )
        file = patient.lower() + '.txt'
        try:
            data = json.load(open(file))

            patientInfo = json.loads(data)
            info = json.dumps(patientInfo, indent=2)

            root = Tk()
            lbl = Label(root, text=info, font="Times32", justify='left')
            lbl.pack()
        except:
            tkMessageBox.showinfo('10MWT', 'sorry, no patient found', icon='warning')
            
def Main():
    global root
 
    root = Tk()
    root.title("10MWT")
    width = 600
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Top = Frame(root, width=600)
    Top.pack(side=TOP)
    stopWatch = StopWatch(root)
    stopWatch.pack(side=TOP)
    Bottom = Frame(root, width=600)
    Bottom.pack(side=BOTTOM)
    Center = Frame(root, width=600)
    Center.pack(side = LEFT)
    Start =  Button(Bottom, text='Start', command=stopWatch.Start, width=10, height=2)
    Start.pack(side=LEFT)
    Stop = Button(Bottom, text='Stop', command=stopWatch.Stop, width=10, height=2)
    Stop.pack(side=LEFT)
    Reset = Button(Bottom, text='Reset', command=stopWatch.Reset, width=10, height=2)
    Reset.pack(side=LEFT)
    Trial = Button(Bottom, text='Save Trial', command=stopWatch.Save, width=10, height=2)
    Trial.pack(side=LEFT)
    Exit = Button(Bottom, text='Exit', command=stopWatch.Exit, width=10, height=2)
    Exit.pack(side=LEFT)
    Title = Label(Top, text="10MWT", font=("arial", 20), fg="white", bg="black")
    Title.pack(fill=X)
    Trials = Label(stopWatch, text="Trials:", font=("arial", 20), fg="white", bg="black")
    Trials.pack(fill=X)

    Search = Button(Top, text='Search for patient', command=stopWatch.DataReader, width=20, height=2)
    Search.pack(side=LEFT)
    Patient = Button(Top, text='New Patient', command=stopWatch.NewPatient, width=20, height=2)
    Patient.pack(side=RIGHT)
    Restart = Button(Top, text='New test', command=stopWatch.Restart, width=20, height=2)
    Restart.pack(side=RIGHT)

    TrialOne = Label(stopWatch, textvariable= stopWatch.timeOne, font=("arial", 15), fg="white", bg="black")
    TrialOne.pack(fill=X)
    TrialTwo = Label(stopWatch, textvariable= stopWatch.timeTwo, font=("arial", 15), fg="white", bg="black")
    TrialTwo.pack(fill=X)
    TrialThree = Label(stopWatch, textvariable= stopWatch.timeThree, font=("arial", 15), fg="white", bg="black")
    TrialThree.pack(fill=X)
    AvgGait = Label(stopWatch, textvariable= stopWatch.avgGait, font=("arial", 15), fg="white", bg="black")
    AvgGait.pack(fill=X)
    root.config(bg="black")
    root.mainloop()



if __name__ == '__main__':
    Main()
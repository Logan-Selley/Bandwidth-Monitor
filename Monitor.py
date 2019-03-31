import time
import psutil
import datetime
import tkinter as tk
from tkinter import *

class Monitor:
    startTime = None
    endTime = None
    running = False
    win = None
    
    def __init__(self):
        self.gui()
        
    def gui(self):
        global win, startTime, running
        win = tk.Tk()
        win.title("Logan's Bandwidth Monitor")
        win.geometry("300x100")
        startBtn = Button(win, text = 'Start Monitoring', command = self.start)
        startBtn.pack()
        
        stopBtn = Button(win, text = 'Stop Monitoring', command = self.stopRunning)
        stopBtn.pack()
        
        resetBtn = Button(win, text = "Reset", command = self.reset)
        resetBtn.pack()
        
        runStatus = Label(win, text = "Running?: " + running)
        runStatus.pack()
        
        startStatus = Label(win, text = "Start Time: " + startTime)
        startStatus.pack()
        
        return win
    
    def start(self):
        print("started")
        self.startRunning()
        self.main()
        
    def main(self):
        print("main")
        
    def startRunning(self):
        global running
        running = True
        print(running)
        return running
    
    def stopRunning(self):
        global running
        running = False
        return running
    
    def reset(self):
        global startTime, endTime, running, win
        startTime = None
        endTime = None
        running = False
        win = None
        return startTime, endTime, running, win
        
    def updateStart(self):
        global startTime
        startTime = datetime.datetime.now()
        return startTime
        
    def end(self):
        global startTime
        endTime = datetime.datetime.now()
        print(endTime)
        print(startTime)
Monitor()
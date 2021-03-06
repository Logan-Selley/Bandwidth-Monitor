import datetime
from tkinter import *
import psutil
from apscheduler.schedulers.background import BackgroundScheduler
''' Event code from https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python'''
from threading import Event
'''
TODO:
make per second readings optional?
'''


class Monitor:
    sched = BackgroundScheduler()
    startTime = None
    endTime = None
    running = False
    exit = Event()
    win = None
    job = None
    runlabel = None
    startlabel = None
    weeklyup = 0
    weeklydown = 0
    totalup = 0
    totaldown = 0
    interval = 1000

    def __init__(self, master):
        self.job = self.sched.add_job(self.printout, 'interval', days=7)
        self.job.pause()
        self.gui(master)

    def gui(self, master):
        self.win = master
        self.win.title("Logan's Bandwidth Monitor")
        self.win.geometry("300x200")
        self.runlabel = StringVar()
        self.runlabel.set(str(self.running))
        self.startlabel = StringVar()
        self.startlabel.set(str(self.startTime))
        start_btn = Button(self.win, text='Start Monitoring', command=self.start)
        start_btn.pack()

        stop_btn = Button(self.win, text='Stop Monitoring', command=self.stoprunning)
        stop_btn.pack()

        run = StringVar()
        run.set(self.running)
        run_status = Label(self.win, text="running?: ", textvariable=self.runlabel)
        run_status.pack()

        start_status = Label(self.win, text= "Start time: ", textvariable=self.startlabel)
        start_status.pack()
        root.mainloop()

    def start(self):
        print("started")
        self.startrunning()
        root.after(1, self.main)

    def main(self):
        print("main")
        print("run")
        print(self.exit)
        if not self.exit.is_set():
            interval = 1
            print("running")
            args = self.poll(interval)
            print(args)
            self.update(*args)
            root.after(1, self.main)

    ''' function sourced from https://github.com/giampaolo/psutil/blob/master/scripts/nettop.py'''
    def poll(self, interval):
        tot_before = psutil.net_io_counters()
        pnic_before = psutil.net_io_counters(pernic=True)
        # sleep some time
        self.exit.wait(interval)
        tot_after = psutil.net_io_counters()
        pnic_after = psutil.net_io_counters(pernic=True)
        return tot_before, tot_after, pnic_before, pnic_after, interval

    def update(self, tot_before, tot_after, pnic_before, pnic_after, interval):
        bytes_sent = tot_after.bytes_sent - tot_before.bytes_sent
        bytes_received = tot_after.bytes_recv - tot_before.bytes_recv
        self.weeklyup += bytes_sent
        self.totalup += bytes_sent
        self.weeklydown += bytes_received
        self.totaldown += bytes_received
        print(self.bytes2human(self.totalup))
        print(self.bytes2human(self.totaldown))

    def printout(self):
        print("print")
        file = open(str(datetime.datetime.today().strftime("%Y%m%d-%H%M%S")), "w")
        file.write("Week's Download: " + self.bytes2human(self.weeklydown) + "\n")
        file.write("Week's Upload: " + self.bytes2human(self.weeklyup) + "\n")
        self.weeklydown = 0
        self.weeklyup = 0
        ''' write weekly variables'''
        ''' think about changing output based on run status'''
        file.close()
        '''reset weekly variables'''

    def startrunning(self):
        self.updatestart()
        self.exit.clear()
        self.job.resume()
        self.weeklyup = 0
        self.weeklydown = 0
        self.totaldown = 0
        self.totalup = 0
        self.running = True
        self.runlabel.set(str(self.running))

    def stoprunning(self):
        self.exit.set()
        self.job.pause()
        self.end()
        self.exitprint()
        self.running = False
        self.runlabel.set(str(self.running))

    def exitprint(self):
        print("exit print")
        file = open(str(datetime.datetime.today().strftime("%Y%m%d-%H%M%S")), "w")
        file.write("Started: " + str(self.startTime) + "\n")
        file.write("Ended: " + str(self.endTime) + "\n")
        file.write("Total Download: " + self.bytes2human(self.totaldown) + "\n")
        file.write("Total Upload: " + self.bytes2human(self.totalup) + "\n")
        self.totaldown = 0
        self.totalup = 0
        self.weeklydown = 0
        self.weeklyup = 0
        self.endTime = None
        self.startTime = None
        self.startlabel.set(str(self.startTime))

        file.close()

    def updatestart(self):
        self.startTime = datetime.datetime.now()
        self.startlabel.set(str(self.startTime))

    '''Does this function even do anything right now?'''
    def end(self):
        self.endTime = datetime.datetime.now()

    ''' function sourced from https://github.com/giampaolo/psutil/blob/master/scripts/nettop.py'''
    def bytes2human(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f %s' % (value, s)
        return '%.2f B' % n


root = Tk()
monitor = Monitor(root)


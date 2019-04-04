import datetime
from tkinter import *
import psutil
from apscheduler.schedulers.blocking import BackgroundScheduler
''' Event code from https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python'''
from threading import Event
'''
TODO:
change running boolean to python event: https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python
make Tkinter gui update somehow to reflect changes in network activity and updated start time and running status
output results to file every week use backgroun scheduler
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
    weeklyup = 0
    weeklydown = 0
    totalup = 0
    totaldown = 0

    def __init__(self, master):
        self.job = self.sched.add_job(self.printout, 'interval', days=7)
        self.job.pause()
        self.gui(master)

    def gui(self, master):
        self.win = master
        self.win.title("Logan's Bandwidth Monitor")
        self.win.geometry("300x200")
        start_btn = Button(self.win, text='Start Monitoring', command=self.start)
        start_btn.pack()

        stop_btn = Button(self.win, text='Stop Monitoring', command=self.stoprunning)
        stop_btn.pack()

        reset_btn = Button(self.win, text="Reset", command=self.reset)
        reset_btn.pack()

        run_status = Label(self.win, text="Running?: " + str(self.running))
        run_status.pack()

        start_status = Label(self.win, text="Start Time: " + str(self.startTime))
        start_status.pack()

    def start(self):
        print("started")
        self.startrunning()
        self.main()

    def main(self):
        print("main")
        try:
            print("run")
            interval = 0
            print(self.exit)
            while not self.exit.is_set():
                print("running")
                args = self.poll(interval)
                print(args)
                self.update(*args)
                interval = 1
        except (KeyboardInterrupt, SystemExit):
            pass

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
        print("refresh")

    def printout(self):
        print("print")
        file = open(str(datetime.datetime.now()), "w")
        file.write("Week's Download: " + self.bytes2human(self.weeklydown))
        file.write("Week's Upload: " + self.bytes2human(self.weeklyup))
        self.weeklydown = 0
        self.weeklyup = 0
        ''' write weekly variables'''
        ''' think about changing output based on run status'''
        file.close()
        '''reset weekly variables'''

    def startrunning(self):
        self.exit.clear()
        self.job.resume()
        self.weeklyup = 0
        self.weeklydown = 0
        self.totaldown = 0
        self.totalup = 0
        self.running = True

    def stoprunning(self):
        self.exit.set()
        self.job.pause()
        self.exitprint()
        self.running = False

    def exitprint(self):
        print("exit print")
        '''total'''

    def reset(self):
        global startTime, endTime, running, win
        startTime = None
        endTime = None
        running = False
        win = None
        return startTime, endTime, running, win

    def updatestart(self):
        global startTime
        startTime = datetime.datetime.now()
        return startTime

    def end(self):
        global startTime
        end_time = datetime.datetime.now()
        print(end_time)
        print(startTime)

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
root.mainloop()

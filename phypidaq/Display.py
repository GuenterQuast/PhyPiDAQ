# -*- coding: utf-8 -*-

'''Class providing graphical display and, optionally, a control interface
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys
import multiprocessing as mp

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
if sys.version_info[0] < 3:
  import Tkinter as Tk
  import tkMessageBox as mbox
  from tkFileDialog import asksaveasfilename
else:
  import tkinter as Tk
  from tkinter import messagebox as mbox
  from tkinter.filedialog import asksaveasfilename

import matplotlib.pyplot as plt, matplotlib.animation as anim


class Display(object):
  '''configure and control graphical data displays'''

  def __init__(self, interval = 0.1, confdict = None, cmdQ = None, datQ=None):
    '''Args: 
         interval:  logging interal, eventually overwritten by entry in confdict
         confdict:  dictionary with configuration
         cmdQ:      multiprocessing Queue for command transfer to caller
         datQ:      multiprocessing Queue for data transfer
    '''

    self.cmdQ = cmdQ
    self.datQ = datQ
    if confdict!=None: 
      self.confdict = confdict      
    else:
      self.confdict={}

# set default options for graphical display
    if 'Interval' not in self.confdict:
      self.confdict['Interval'] = interval
    else:
      interval = self.confdict['Interval']
    if interval < 0.05:
      print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
      self.confdict['Interval'] = 0.05

    if 'XYmode' not in self.confdict:  # default is XY mode off
      self.confdict['XYmode'] = False

    if 'DisplayModule' not in self.confdict: # default display is DataLogger
      self.confdict['DisplayModule'] = 'DataLogger'

    if 'startActive' not in self.confdict:  # default is to start in Paused mode
      self.confdict['startActive'] = False

# set channel properties
    if 'NChannels' not in self.confdict:  
      self.confdict['NChannels'] = 1

    NC = self.confdict['NChannels']
    if 'ChanLimits' not in self.confdict:
      self.confdict['ChanLimits'] = [ [0., 5.] ]*NC
    if 'ChanNams' not in self.confdict:
      self.confdict['ChanNams'] = ['']*NC 
    if 'ChanUnits' not in self.confdict:
      self.confdict['ChanUnits'] = ['V']*NC

    if 'ChanLabels' not in self.confdict:
      self.confdict['ChanLabesl'] = ['']*NC

# set display control options
    if 'startActive' not in self.confdict:  # start with active data taking
      self.self.confdict['startActive'] = True

    if 'DAQCntrl' not in self.confdict:  # no run control buttons
      self.confdict['DAQCntrl'] = False

  def init(self):
    '''create data transfer queue and start display process'''
 
    if self.datQ == None: 
      self.datQ = mp.Queue(1) # Queue for data transfer to sub-process
    DisplayModule = self.confdict['DisplayModule']
    self.procs=[]
    self.procs.append(mp.Process(name=DisplayModule, 
                                 target = self.mpTkDisplay) )

    for prc in self.procs:
      prc.deamon = True
      prc.start()
      # print(' -> starting subprocess ', prc.name, ' PID=', prc.pid)

  def show(self, dat): 
    # send data to display process 
    self.datQ.put(dat)
    time.sleep(0.00005) # !!! waiting time to make data transfer reliable
    
  def close(self):
    # shut-down sub-process(es) 
    for p in self.procs:
      if p.is_alive():
        p.terminate()
        # print('    terminating ' + p.name)

  def mpTkDisplay(self):
    ''' Tk background process for graphical display of data

        data is passed via multiprocessing.Queue
    '''

    Q = self.datQ    # multiprocessing.Queue() for data 
    conf = self.confdict # configuration
    cmdQ = self.cmdQ  # Queue to send commands back to calling process
 
    ModuleName = conf['DisplayModule'] # name of the display module

    # import relevant library
    try:
      cmnd ='from .'+ ModuleName + ' import *' 
      exec(cmnd, globals(), locals())
    except Exception as e:
      print(' !!! TkDisplay: failed to import module - exiting')
      print(str(e))
      sys.exit(1)

    try:
      cmnd = 'global DG; DG = ' + ModuleName +'(conf)'
      exec(cmnd, globals(), locals()) 
    except Exception as e: 
      print(' !!! TkDisplay: failed to initialize module - exiting')
      print(str(e))
      sys.exit(1)


    # Generator to provide data to animation
    def yieldEvt_fromQ():
  # receive data via a Queue from package mutiprocessing
      cnt = 0
      lagging = False
      Tlast = time.time()
      
      while True:
        if not Q.empty():
          data = Q.get()
          if type(data) != np.ndarray:
            break # received end event
          cnt+=1
          yield (cnt, data)
        else:
          yield None # send empty event if no new data

  # check timing precision 
        T = time.time()
        dt = T - Tlast
        if dt - interval < interval*0.01:
          if lagging: 
            LblStatus.config(text='')
          lagging=False
        else:
          lagging=True
          LblStatus.config(text='! lagging !', fg='red')
        Tlast = T
        
  # end of yieldEvt_fromQ
      sys.exit()

  # define bindings for graphical command buttons
  # set initial state
    def setInitialPaused(): # usually, start in Paused mode
      buttonP.config(text='paused', fg='grey', state=Tk.DISABLED)
      buttonR.config(state=Tk.NORMAL, text='Run')

    def setPaused():
      buttonP.config(text='paused', fg='grey', state=Tk.DISABLED)
      buttonR.config(state=Tk.NORMAL, text='Resume')

    def setRunning():
      buttonP.config(text='Pause', underline=0, fg='blue', state=Tk.NORMAL)
      buttonR.config(state=Tk.DISABLED, text='Resume')

    def cmdResume(_event=None):
      cmdQ.put('R')
      setRunning()
      self.t0 = time.time()

    def cmdPause(_event=None):
      cmdQ.put('P')
      setPaused() 
   
    def cmdEnd(_event=None):
      cmdQ.put('E')

    def cmdSaveData(_event=None):
      cmdQ.put('s')
      setPaused() 

    def cmdSaveGraph(_event=None):
      cmdPause()
      try:
        filename = asksaveasfilename(initialdir='.', initialfile='DGraphs.png', 
               title='select file name')
        figDG.savefig(filename) 
      except Exception as e:
        print(str(e))
        pass

   # a simple clock
    def clkLabel(TkLabel):
      self.t0=time.time()
      def clkUpdate():
        dt = int(time.time() - self.t0)
        # datetime = time.strftime('%y/%m/%d %H:%M', time.localtime(t0))
        TkLabel.config(text = ' ' + str(dt) + 's  ', fg='blue' )
        TkLabel.after(1000, clkUpdate)
      clkUpdate()
   
# ------- executable part -------- 
  #  print(' -> mpTkDisplay starting')

    interval = conf['Interval']
    WaitTime = interval * 1000 # in ms
  
    if 'startActive' in conf:
      startActive = conf['startActive'] # start in active mode
    else:
      startActive = False

    if 'DAQCntrl' in conf:       # enable control buttons
      DAQCntrl = conf['DAQCntrl']
    else:
      DAQCntrl = True

    figDG = DG.fig

  # generate a simple window for graphics display as a tk.DrawingArea
    root = Tk.Tk()
    root.wm_title(ModuleName)

  # handle destruction of top-level window
    def _delete_window():
      if mbox.askokcancel("Quit", "Really destroy  main window ?"):
       print("Deleting main window")
       root.destroy()
    root.protocol("WM_DELETE_WINDOW", _delete_window)

  # initialize status and control field
    frame = Tk.Frame(master=root)
    frame.grid(row=0, column=9)
    frame.pack(padx=5, side=Tk.BOTTOM)
    if DAQCntrl:
  # initialize Comand buttons
      buttonE = Tk.Button(frame, text='End', underline=0, fg='red', command=cmdEnd)
      buttonE.grid(row=0, column=8)
      root.bind('E', cmdEnd)

      blank1 = Tk.Label(frame, width=5, text="")
      blank1.grid(row=0, column=7)

      if 'bufferData' in self.confdict:
       if self.confdict['bufferData'] != None:
         buttonSvDa = Tk.Button(frame, width=7, text='saveData', 
                        underline=0, fg='purple', command=cmdSaveData)
         buttonSvDa.grid(row=0, column=6)
         root.bind('s', cmdSaveData)
      else:
        blank2 = Tk.Label(frame, width=5, text="")
        blank2.grid(row=0, column=6)

      buttonSvGr = Tk.Button(frame, width=7, text='SaveGraph', underline=0, fg='purple',
                           command=cmdSaveGraph)
      buttonSvGr.grid(row=0, column=5)
      root.bind('S', cmdSaveGraph)

      blank3 = Tk.Label(frame, width=5, text="")
      blank3.grid(row=0, column=4)

      buttonP = Tk.Button(frame, width=7, text='Pause', underline=0,  fg='blue',
                   command=cmdPause)
      buttonP.grid(row=0, column=3)
      root.bind('P', cmdPause)

      buttonR = Tk.Button(frame, width=7, text='Resume', underline=0, fg='blue',
                    command=cmdResume)
      buttonR.grid(row=0, column=2)
      buttonR.config(state=Tk.DISABLED)
      root.bind('R', cmdResume)

  # set up fields for status and clock
    clock = Tk.Label(frame, width=10)
    clock.grid(row=0, column=9)
    LblStatus = Tk.Label(frame, width=13, text="")
    LblStatus.grid(row=0, column=0)

  # set up window for graphics output
    canvas = FigureCanvasTkAgg(figDG, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

  # set initial state
    if not startActive and DAQCntrl:
      setInitialPaused() # start in Paused mode

  # set up matplotlib animation
    tw = max(WaitTime-100., 0.5) # smaller than WaitTime to allow for processing
    DGAnim = anim.FuncAnimation(figDG, DG, yieldEvt_fromQ,
                         interval = tw, init_func = DG.init,
                         blit=True, fargs=None, repeat=True, save_count=None)
                       # save_count=None is a (temporary) work-around 
                       #     to fix memory leak in animate
    try:
      clkLabel(clock) # start clock

      Tk.mainloop()   # start event loop
    except Exception as e:
      print('*==* mpTkDisplay running ' + ModuleName + ': forced exit')
      print(str(e))
    sys.exit()

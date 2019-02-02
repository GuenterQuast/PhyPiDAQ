# -*- coding: utf-8 -*-

'''exectue Display Module in Tkinter window '''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, numpy as np

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


def mpTkDisplay(Q, conf,  
                ModuleName='DataGraphs', cmdQ=None):
  ''' data passed via multiprocessing.Queue
    Args:
      Q:    multiprocessing.Queue()   
      conf: Config dictionary for Display Module
      ModuleName: name of Display Module to start
      cmdQ: Queue to send commands back to calling process
  '''

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

    while True:
      T0 = time.time()
      if not Q.empty():
        data = Q.get()
        if type(data) != np.ndarray:
          break # received end event
        cnt+=1
        yield (cnt, data)
      else:
        yield None # send empty event if no new data

# guarantee correct timing 
      dtcor = interval - time.time() + T0
      if dtcor > 0. :  
        time.sleep(dtcor) 
        if lagging: 
          LblStatus.config(text='')
          lagging=False
      else:
        lagging=True
        LblStatus.config(text='! lagging !', fg='red')
# end of yieldEvt_fromQ
    sys.exit()

# define bindinds for graphical command buttons
# set initial state
  def setInitialPaused(): # usually, start in Paused mode
    buttonP.config(text='paused', fg='grey', state=Tk.DISABLED)
    buttonR.config(state=Tk.NORMAL, text='Resume/start')

  def setPaused():
    buttonP.config(text='paused', fg='grey', state=Tk.DISABLED)
    buttonR.config(state=Tk.NORMAL, text='Resume')

  def setRunning():
    buttonP.config(text='Pause', underline=0, fg='blue', state=Tk.NORMAL)
    buttonR.config(state=Tk.DISABLED)

  def cmdResume(_event=None):
    cmdQ.put('R')
    setRunning()

  def cmdPause(_event=None):
    cmdQ.put('P')
    setPaused() 
   
  def cmdEnd(_event=None):
    cmdQ.put('E')

  def cmdSave(_event=None):
    cmdPause()
    try:
      filename = asksaveasfilename(initialdir='.', initialfile='DGraphs.png', 
               title='select file name')
      figDG.savefig(filename) 
    except Exception as e:
      print(str(e))
      pass
 
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
  frame.grid(row=0, column=8)
  frame.pack(padx=5, side=Tk.BOTTOM)
  if DAQCntrl:
# initialize Comand buttons
    buttonE = Tk.Button(frame, text='End', underline=0, fg='red', command=cmdEnd)
    buttonE.grid(row=0, column=8)
    root.bind('E', cmdEnd)

    blank = Tk.Label(frame, width=7, text="")
    blank.grid(row=0, column=7)

    clock = Tk.Label(frame)
    clock.grid(row=0, column=5)

    buttonSv = Tk.Button(frame, width=8, text='Save', underline=0, fg='purple',
                   command=cmdSave)
    buttonSv.grid(row=0, column=4)
    root.bind('S', cmdSave)

    buttonP = Tk.Button(frame, width=8, text='Pause', underline=0,  fg='blue',
                   command=cmdPause)
    buttonP.grid(row=0, column=3)
    root.bind('P', cmdPause)

    buttonR = Tk.Button(frame, width=8, text='Resume', underline=0, fg='blue',
                    command=cmdResume)
    buttonR.grid(row=0, column=2)
    buttonR.config(state=Tk.DISABLED)
    root.bind('R', cmdResume)

  # set up fild for status
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
    Tk.mainloop()
  except Exception as e:
    print('*==* mpTkDisplay running ' + ModuleName + ': forced exit')
    print(str(e))
  sys.exit()

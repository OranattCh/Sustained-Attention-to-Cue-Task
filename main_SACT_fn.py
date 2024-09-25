from psychopy import visual, core, event, sound

import numpy as np
import random as random
from multiprocessing.connection import wait
# from psychopy import parallel

class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        
class SACTExp:
    def _fixStim(self):
        text='+'
        font='Open Sans'
        color='black'
        
        return visual.TextStim(self.win, text=text, font=font, height=0.1,color=color, colorSpace='rgb', opacity=None)        
        
    def _beepStim(self):
        
        print('Can ignore this msg: init_beepStim')
                
        return sound.Sound(self.exp_location+'prebeep8bit.wav', secs=self.tBeep, volume = 1.0,stereo=True, hamming=True)
    
    def _cueStim(self):        
        cue_image = self.exp_location+'images/cue.png'
            
        return visual.ImageStim(self.win, cue_image, size=(0.1, 0.1),texRes=128.0, interpolate=True)

    def _distractionStim(self):
        text='*'
        font='Open Sans'
        color='white'
        
        return visual.TextStim(self.win, text=text, font=font, height=0.15,color=color, colorSpace='rgb', opacity=None)
    
    def _blankStim(self):
        text=''
        font='Open Sans'
        color='white'
        
        return visual.TextStim(self.win, text=text, font=font, height=0.05,color=color, colorSpace='rgb', opacity=None)
    
    def _targetStim(self):
               
        print('Can ignore this msg: init_targetStim')
        
        return visual.ImageStim(self.win, size=(0.25, 0.25),texRes=128.0, interpolate=True)
    
    def _targetMaskStim(self):        
        targetMask_image =self.exp_location+'images/Mask.bmp'
            
        return visual.ImageStim(self.win, targetMask_image, size=(0.25, 0.25),texRes=128.0, interpolate=True)
    
    def _respB(self):
        resp_image = self.exp_location+'images/target_B.jpg'
        resp_x = -0.5;  resp_y = 0
        target_B=visual.ImageStim(self.win, resp_image, name='target_B', pos=(resp_x, resp_y), size=(0.25, 0.25),texRes=128.0, interpolate=True)
        return target_B
    
    def _respD(self):
        resp_image = self.exp_location+'images/target_D.jpg'
        resp_x = -0.18; resp_y = 0
        target_D=visual.ImageStim(self.win, resp_image, name='target_D', pos=(resp_x, resp_y), size=(0.25, 0.25),texRes=128.0, interpolate=True)
        return target_D
    
    def _respP(self):
        resp_image = self.exp_location+'images/target_P.jpg'
        resp_x = 0.18;  resp_y = 0
        target_P=visual.ImageStim(self.win, resp_image, name='target_P', pos=(resp_x, resp_y), size=(0.25, 0.25),texRes=128.0, interpolate=True)
        return target_P
    
    def _respR(self):
        resp_image = self.exp_location+'images/target_R.jpg'
        resp_x = 0.5;   resp_y = 0
        target_R=visual.ImageStim(self.win, resp_image, name='target_R', pos=(resp_x, resp_y), size=(0.25, 0.25),texRes=128.0, interpolate=True)
        return target_R
    
    def __init__(self, mon, win, winsize, refreshRate, clock, startTime, mymouse, exp_location, logfile=None):
        self.mon = mon
        self.win = win
        self.winsize = winsize
        self.refreshRate = refreshRate
        self.frameTime = 1.0 / float(refreshRate)
        self.clock = clock
        self.startTime = startTime
        self.mymouse = mymouse
        
        self.exp_location = exp_location
        self.logfile = logfile

        # if logfile:
        #     logfile.write("wallt;t0;warning;position;direction;congruency;d1;ct;d2;rt;tf;response\n")
        # else:
        #     print("wallt;t0;warning;position;direction;congruency;d1;ct;d2;rt;tf;response")

        # Timings for each 'procedure' [in seconds]
        # tFix and tCue will defind later, as vary from condition
        self.tBeep = 0.3
        self.tCueDy = 1.5
        self.tDistraction = 0.1
        self.tTarget = 0.125
        self.tTargetMark = 1
                
        # Set up the experimental combinations, creating a list of all combinations of cue, location, direction and flankers
        self.procedures = [Bunch()] * 128
        i = 0
        for fix_dur in ('sec2', 'sec3'):
            for cue_dur in ('sec2', 'sec4', 'sec8', 'sec12'):
                for cue_loc in ('topL', 'topR', 'bottomL', 'bottomR'):
                    for target in ('B', 'D', 'P', 'R'):
                        self.procedures[i]=Bunch(fix_dur=fix_dur, cue_dur=cue_dur, cue_loc=cue_loc, target=target)
                        i+=1

        # # Create stimuli to be used
        self.visFix = self._fixStim()
        self.visBeep = self._beepStim()
        self.visCue = self._cueStim()
        self.visDistraction = self._distractionStim()
        self.visBlank = self._blankStim()        
        self.visTarget = self._targetStim()
        self.visTargetMask = self._targetMaskStim()
        
        self.visRespBStim = self._respB()
        self.visRespDStim = self._respD()
        self.visRespPStim = self._respP()
        self.visRespRStim = self._respR()
        
    def _oneProcedure(self, condition, short=False):
        def waitAndFlip(t):
            core.wait(t - self.clock.getTime() - self.frameTime, self.frameTime/2.0)
            self.win.flip()

            return self.clock.getTime()

        quit = False

        # print('condition')
        # print(condition.fix_dur)
        # print(condition.cue_dur)
        # print(condition.cue_loc)
        # print(condition.target)
        
        # parallel.setData(100) # ---------- Trigger trial started ----------
        print('TRIGGER #100')

        self.visFix.draw()
        self.win.flip()
        t0 = self.clock.getTime()

        if condition.fix_dur =='sec2':
            tFix=2
        elif condition.fix_dur =='sec3':
            tFix=3

        # print('check: fix')
        # print(tFix)

        d1 = waitAndFlip(t0 + tFix) -t0
        
        self.visBeep.play()
        core.wait(self.tBeep)
        self.visBeep.stop()
        # print('check: beep')
        self.visBlank.draw()
        d2 = waitAndFlip(t0 + tFix + self.tBeep) -t0 -d1
        
        # parallel.setData(101) # ---------- Trigger beeped and cue appear ----------
        print('TRIGGER #101')
        
        if condition.cue_loc == 'topL':
            # print('check pos')
            pos_x = -0.6;   pos_y = 0.4
            self.visTarget.pos = (pos_x,pos_y)
            self.visTargetMask.pos = (pos_x,pos_y)
            self.visCue.pos = (pos_x,pos_y)
            # print(pos_x)
            # print(pos_y)
        elif condition.cue_loc =='topR':
            # print('check pos')
            pos_x = 0.6;   pos_y = 0.4
            self.visTarget.pos = (pos_x,pos_y)
            self.visTargetMask.pos = (pos_x,pos_y)
            self.visCue.pos = (pos_x,pos_y)
            # print(pos_x)
            # print(pos_y)
        elif condition.cue_loc =='bottomL':
            # print('check pos')
            pos_x = -0.6;   pos_y = -0.4
            self.visTarget.pos = (pos_x,pos_y)
            self.visTargetMask.pos = (pos_x,pos_y)
            self.visCue.pos = (pos_x,pos_y)
            # print(pos_x)
            # print(pos_y)
        elif condition.cue_loc =='bottomR':
            # print('check pos')
            pos_x = 0.6;   pos_y = -0.4
            self.visTarget.pos = (pos_x,pos_y)
            self.visTargetMask.pos = (pos_x,pos_y)
            self.visCue.pos = (pos_x,pos_y)
            # print(pos_x)
            # print(pos_y)
        
        start_size = 100 # pixels
        mid_size = 60 # pixels
        end_size = 20 # pixels
        
        if self.win.useRetina:
            posPix_x = pos_x * (self.winsize[1]/2)
            posPix_y = pos_y * (self.winsize[1]/2)
        else:
            posPix_x = pos_x * (self.winsize[1])
            posPix_y = pos_y * (self.winsize[1])
        
        diff_size_1 = start_size - mid_size
        diff_size_2 = mid_size - end_size
        
        nFrame = int((self.tCueDy/2) * (1/self.frameTime)) # number of frame needed
        shrink_1 = diff_size_1 / nFrame # shrink per frame
        shrink_2 = diff_size_2 / nFrame # shrink per frame
        
        # line shrink
        for i in range(nFrame):
            border_size = start_size - (i * shrink_1)
            hole_size = border_size - 3
            
            visual.Circle(win=self.win, radius=border_size, pos=(posPix_x,posPix_y), units='pix',fillColor=[-0.2,-0.2,-0.2],lineColor=[-0.2,-0.2,-0.2], edges=128).draw()
            visual.Circle(win=self.win, radius=hole_size, pos=(posPix_x,posPix_y), units='pix',fillColor=[0,0,0],lineColor=[0,0,0], edges=128).draw()
            self.win.flip()
#            print(border_size)

        mid_size_update = border_size
        # hole shrink
        for j in range(nFrame):
            border_size = mid_size_update
            hole_size = mid_size_update - (j * shrink_2)
            
            visual.Circle(win=self.win, radius=border_size, pos=(posPix_x,posPix_y), units='pix',fillColor=[-0.2,-0.2,-0.2],lineColor=[-0.2,-0.2,-0.2], edges=128).draw()
            visual.Circle(win=self.win, radius=hole_size, pos=(posPix_x,posPix_y), units='pix',fillColor=[0,0,0],lineColor=[0,0,0], edges=128).draw()
            self.win.flip()
#            print(hole_size)
            
        # self.visCue.draw()
        visual.Circle(win=self.win, radius=border_size, pos=(posPix_x,posPix_y), units='pix',fillColor=[-0.2,-0.2,-0.2],lineColor=[-0.2,-0.2,-0.2], edges=128).draw()
        visual.Circle(win=self.win, radius=hole_size, pos=(posPix_x,posPix_y), units='pix',fillColor=[0,0,0],lineColor=[0,0,0], edges=128).draw()
        d3 = waitAndFlip(t0 + tFix + self.tBeep + self.tCueDy) -t0 -d1 -d2
        
        if condition.cue_dur =='sec2':
            tCue = 2
        elif condition.cue_dur =='sec4':
            tCue = 4
        elif condition.cue_dur =='sec8':
            tCue = 8
        elif condition.cue_dur =='sec12':
            tCue = 12
            
        # print('check: showed cue')
        # print(tCue)
        
        self.visDistraction.draw()
        d4 = waitAndFlip(t0 + tFix + self.tBeep + self.tCueDy + tCue) -t0 -d1 -d2 -d3
        # parallel.setData(102) # ---------- Trigger distractor appeared ----------
        print('TRIGGER #102')
        self.visBlank.draw()
        d5 = waitAndFlip(t0 + tFix + self.tBeep + self.tCueDy + tCue + self.tDistraction*1) -t0 -d1 -d2 -d3 -d4
        self.visDistraction.draw()
        d6 = waitAndFlip(t0 + tFix + self.tBeep + self.tCueDy + tCue + self.tDistraction*2) -t0 -d1 -d2 -d3 -d4 -d5
        # print('check: showed distraction')
        
        if condition.target == 'B':
            self.visTarget.image = self.exp_location+'images/cue_B.jpg'
        elif condition.target == 'D':
            self.visTarget.image = self.exp_location+'images/cue_D.jpg'
        elif condition.target == 'P':
            self.visTarget.image = self.exp_location+'images/cue_P.jpg'
        elif condition.target == 'R':
            self.visTarget.image = self.exp_location+'images/cue_R.jpg'
        
        self.visTarget.draw()
        d7 = waitAndFlip(t0 + tFix + self.tBeep + self.tCueDy + tCue + self.tDistraction*3) -t0 -d1 -d2 -d3 -d4 -d5 -d6    
        # print('check: showed Target')
        
        self.visTargetMask.draw()
        d8 = waitAndFlip(t0 + tFix + self.tBeep + self.tCueDy + tCue + self.tDistraction*3 + self.tTarget) -t0 -d1 -d2 -d3 -d4 -d5 -d6 -d7
        # print('check: showed TargetMask')
        
        self.visRespBStim.draw()
        self.visRespDStim.draw()
        self.visRespPStim.draw()
        self.visRespRStim.draw()
        d9 = waitAndFlip(t0 + d1 + self.tBeep + self.tCueDy + tCue + self.tDistraction*3 + self.tTarget + self.tTargetMark) -t0 -d1 -d2 -d3 -d4 -d5 -d6 -d7 -d8
        # print('check: showed resp')
        
        while self.mymouse.getPressed()[0]==0:
            # visual.TextStim(self.win,text='Wait mouse response').draw()
            # print('wait resp')
            mouseFlag = False
            # self.win.flip()

        if self.mymouse.getPressed()[0]==1:
            mouseFlag = True
            
            pos=self.mymouse.getPos()
            resp_x=pos[0]
            resp_y=pos[1]
            # print(pos)
            # visual.TextStim(self.win,text='got mouse').draw()
            # parallel.setData(103) # ---------- Trigger response received ----------
            print('TRIGGER #103')
            rt = self.clock.getTime() -t0 -d1 -d2 -d3 -d4 -d5 -d6 -d7 -d8 -d9
            # self.win.flip()
            
            # if (resp_y > -0.63 and resp_y < -0.37):
            #     # win = [1280,720]
            #     if (resp_x > -1.51 and resp_x < -1.26) and condition.target =='B':
            #         resp='OK'
            #     elif (resp_x > -1.19 and resp_x < -0.94) and condition.target =='D':
            #         resp='OK'
            #     elif (resp_x > -0.83 and resp_x < -0.58) and condition.target =='P':
            #         resp='OK'
            #     elif (resp_x > -0.51 and resp_x < -0.26) and condition.target =='R':
            #         resp='OK'
                
            # #     # win = [1024,768]
            # #    if (resp_x > -1.29 and resp_x < -1.04) and condition.target =='B':
            # #        resp='OK'
            # #    elif (resp_x > -0.97 and resp_x < -0.72) and condition.target =='D':
            # #        resp='OK'
            # #    elif (resp_x > -0.61 and resp_x < -0.36) and condition.target =='P':
            # #        resp='OK'
            # #    elif (resp_x > -0.29 and resp_x < -0.04) and condition.target =='R':
            # #        resp='OK'
            #     else:
            #         resp='NOK'
            # else:
            #     resp='NOK'

            # win - exp system
            if (resp_y > -0.125 and resp_y < 0.125):
                if (resp_x > -0.63 and resp_x < -0.375) and condition.target =='B':
                    resp='OK'
                elif (resp_x > -0.31 and resp_x < -0.06) and condition.target =='D':
                    resp='OK'
                elif (resp_x > 0.05 and resp_x < 0.3) and condition.target =='P':
                    resp='OK'
                elif (resp_x > 0.37 and resp_x < 0.62) and condition.target =='R':
                    resp='OK'
                else:
                    resp='NOK'
            else:
                resp='NOK'
                
        tf = self.clock.getTime() - t0
                    
        # keys = event.waitKeys()
        # if keys is not None:
        #     if keys[0] == 'escape':
        #         quit = True
        
        if quit:
            return None
        else:
            return (Bunch(condition=condition, t0=t0, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, d7=d7, d8=d8, d9=d9, rt=rt, tf=tf, resp_x=resp_x, resp_y=resp_y, resp=resp))
        
    def practiceBlock(self, maxrun=3): # maxrun <= 128 procedures        
        for i in random.sample(range(len(self.procedures)), len(self.procedures)):
            res = self._oneProcedure(self.procedures[i], True)

            if res is None:
                return False

            self.win.flip()
            if res.resp=='OK':
                visual.TextStim(self.win, color='black', alignHoriz='center', wrapWidth=None, height=0.05, text="Correct reply (%0.3fs)" % (res.rt)).draw()
            elif res.resp=='NOK':
                visual.TextStim(self.win, color='black', alignHoriz='center', wrapWidth=None, height=0.05, text="Incorrect reply (%0.3fs)" % (res.rt)).draw()
            else:
                visual.TextStim(self.win, color='black', alignHoriz='center', wrapWidth=None, height=0.05, text="No timely response recorded").draw()
            self.win.flip()
            core.wait(2)

            maxrun -= 1
            if maxrun==0:
                return True
            
    def fullExperiment(self, maxrun=5):
        tr=0
        expData = np.zeros((len(self.procedures), 22))
        
        for i in random.sample(range(len(self.procedures)), len(self.procedures)):
            res = self._oneProcedure(self.procedures[i])
            if res is None:
                return None
            cond = self.procedures[i]
        
            if cond.fix_dur=='sec2':
                fix_duration = 2
            elif cond.fix_dur=='sec3':
                fix_duration = 3
                
            if cond.cue_dur=='sec2':
                cue_duration = 2
            elif cond.cue_dur=='sec4':
                cue_duration = 4
            elif cond.cue_dur=='sec8':
                cue_duration = 8
            elif cond.cue_dur=='sec12':
                cue_duration = 12
                
            if cond.cue_loc=='topL':
                cue_location = 1
            elif cond.cue_loc=='topR':
                cue_location = 2
            elif cond.cue_loc=='bottomL':
                cue_location = 3
            elif cond.cue_loc=='bottomR':
                cue_location = 4

            if cond.target=='B':
                target = 1
            elif cond.target=='D':
                target = 2
            elif cond.target=='P':
                target = 3
            elif cond.target=='R':
                target = 4
                
            expData[tr] = (i, tr+1, fix_duration, cue_duration, cue_location, target, 
                           res.t0, res.d1, res.d2, res.d3, res.d4, res.d5, res.d6, res.d7, res.d8, res.d9, res.rt, res.tf, res.resp_x, res.resp_y, 1 if res.resp=='OK' else 0, 0 if res.resp is None else 1)

            if maxrun is not None:
                maxrun -= 1
                tr +=1
                if maxrun==0:
                    break
            elif maxrun is None:
                tr +=1

        # return expData[expData[:,-1]==1]
        return expData[expData[:,1]>0]
        # return expData
    
    _instructions1='SACT instruction' + \
        '\n\n' + \
        'Press any key to go to the next page.'
    
    _instructions2='Proceeding to the practice session' + \
        '\n\n' + \
        'Press any key to start' + \
        '\n' + \
        'or hit the "escape" key to go directly to the experiment session.'
    
    def displayText(self, text, noWait=False, time=2):
        self.win.flip()
        visual.TextStim(self.win, alignHoriz='center', wrapWidth=None, height=0.05, color='black', text=text).draw()
        self.win.flip()
        
        if noWait:
            core.wait(time)
            self.win.flip()
            return False
        else:
            keys = event.waitKeys()
            self.win.flip()
            return keys[0]=='escape'
        
    def displayInstructions(self):
        if not self.displayText(self._instructions1):
            noPractice = self.displayText(self._instructions2)
        else:
            noPractice = True
        return noPractice
    
        
        
        
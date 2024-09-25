'''
    SACT Note:
        The SACT was set to run 2 sessions: practice and experiment session.
            - Data from practice session will not be saved.
            - Participant will receive feedback in practice session, but not in experiment session.
            - 'maxrun' variable in SACT_fn.py defines number of trial for both practice and experiment sessions.
        Timestamp and response are saved in excel sheet.
        Data will be overwritten if there is existing file.
        
        Component saved in .xlsx:
            index: index of the procedure, [0-128] combination
            trial: trial order
            
            fix_duration: [2, 3] s
            cue_duration: [2, 4, 8, 12] s
            cue_location: [1] topL, [2] topR, [3] bottomL, [4] bottomR
            target: [1] B, [2] D, [3] P, [4] R
                        
            t0: starting time
            d1: fix_sign time (2, 3 s)
            d2: beep time (300 ms)
            d3: dynamic circle time (1500 ms)
            d4: cue time (2, 4, 8, 12 s)
            d5: distraction time - on (100 ms)
            d6: distraction time - off (100 ms)
            d7: distraction time - on (100 ms)
            d8: target time (125 ms)
            d9: target mask time (1 s)
            rt: reaction time
            tf: total trial time
            
            resp_x, resp_y: mouse click position            
            accuracy: [1] correct response, [0] incorrect or no response
            response: [1] response received, [0] no response

    Connection with cognionics headset:
        Trigger #0 - study starts
        Trigger #1 - start practice session
        Trigger #2 - start experiment session
        
        Trigger #100 - fixation sign appears on screen
        Trigger #101 - cue appears on screen
        Trigger #102 - distraction sign appears on screen
        Trigger #103 - participant attempts response
    
    ********** Need create env for psychopy or run in standalone APP **********
'''
# %%
# # ---------- import important libs ----------
import sys, time
import numpy as np
import pandas as pd

from psychopy import gui, visual, core, event, monitors, data

sys.path.append('/Users/oranattch/Documents/GitRepo/Sustained-Attention-to-Cue-Task/')
# sys.path.append('C:/Users/SINAPSE/Documents/GitRepo/Sustained-Attention-to-Cue-Task/')
from main_SACT_fn import SACTExp

# from psychopy import parallel # for headset connection
# ---------- INIT COGNIONICS ----------
# Connect to Cognionics
#parallel.setPortAddress(0xDFB8)
#port = parallel.ParallelPort(address=0xDFB8)

# create participant info dialog
expInfo = {'Participant_Code': '', 'Session': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title='SACT')
if dlg.OK == False:
    core.quit()
par_info = 'ALERT_SACT_S%s_P%s' % (expInfo['Session'], expInfo['Participant_Code'])

exp_location = '/Users/oranattch/Documents/GitRepo/Sustained-Attention-to-Cue-Task/'
# exp_location = 'C:/Users/SINAPSE/Documents/GitRepo/Sustained-Attention-to-Cue-Task/'

# init monitor
winsize = [1920,1080]#[2560,1600]#[1440,900]#[1280,720]#[1024,768]
mon = monitors.Monitor('testMonitor', distance=57, width=30)
mon.setDistance(57)
mon.setWidth(30)
mon.setSizePix(winsize)
win = visual.Window(winsize, waitBlanking=True, winType='pyglet', fullscr=True, 
                    color=[0,0,0], colorSpace='rgb', blendMode='avg', units='height', monitor=mon)

# check screen timing
pw = visual.TextStim(win, alignHoriz='center', wrapWidth=None, height=0.05, color='black', 
                    text="Please wait (checking screen timing)...")
pw.autoDraw = True
pw.draw()
win.flip()
refresh = win.getActualFrameRate(nIdentical=50, nMaxFrames=900, nWarmUpFrames=100, threshold=1)
pw.autoDraw = False
win.flip()
globalClock = core.Clock()
startTime = time.time()
now = globalClock.getTime()
if now > 0.001:
    sys.stderr.write("WARNING: Your machine seems a little slow; just looking at the watch takes more than 1 mS (%.3f)!\n" %now)
else:
    print("Internal initial timing offset is not to worry about (only %0.6f s)" %now)

# init mouse
mymouse=event.Mouse(win=win)

#parallel.setData(0) # ---------- Trigger starts study ----------
print('TRIGGER #0')

exp = SACTExp(mon, win, winsize, refresh, globalClock, startTime, mymouse, exp_location)

# ---------- START STUDY ----------
# show instruction
noPractice = exp.displayInstructions()
allData = None

# ---------- PRACTICE SESSION ----------
if noPractice:
    sys.stderr.write("Skipped practice on participant's request\n")
else:
    exp.displayText("Starting practice in 2 seconds", noWait=True, time=2)
    # parallel.setData(1) # ---------- Trigger starts practice ----------
    print('TRIGGER #1')
    if not exp.practiceBlock():
        sys.stderr.write("Shortened practice on participant's request\n")

# ---------- EXPER SESSION ----------
exp.displayText("Starting experiment...\n\nHit any key when ready to start.")
core.wait(1)

# parallel.setData(2) # ---------- Trigger starts blk ----------
print('TRIGGER #2')
allData = None
block = exp.fullExperiment()

if block is not None:
    if allData is None:
        allData = block
    else:
        allData = np.concatenate((allData, block))
else:
    print('ERROR: no receive data')

# store data for save after exper end
save_data = pd.DataFrame({'index':allData[:,0], 'trial':allData[:,1],
                            'fix_duration':allData[:,2],'cue_duration':allData[:,3],'cue_location':allData[:,4],'target':allData[:,5],
                            't0':allData[:,6], 'd1':allData[:,7],'d2':allData[:,8],'d3':allData[:,9],'d4':allData[:,10],'d5':allData[:,11],
                            'd6':allData[:,12],'d7':allData[:,13],'d8':allData[:,14],'d9':allData[:,15],
                            'rt':allData[:,16],'tf':allData[:,17],'resp_x':allData[:,18],'resp_y':allData[:,19],
                            'accuracy':allData[:,20], 'response':allData[:,21]})
                                    
# ---------- SAVE EXPER ----------
# in .xlsx file
# saveFileName = 'test_SACTExp_tr3.xlsx'
saveFileName = 'data/' + par_info + '.xlsx'
# with pd.ExcelWriter(exp_location+saveFileName,if_sheet_exists='replace') as writer: # replace existing sheets/files
with pd.ExcelWriter(exp_location+saveFileName) as writer: # replace existing sheets/files
    save_data.to_excel(writer, sheet_name='block1', index=False)

print("----- SAVED & END EXP ------")
exp.displayText("End cognitive task\n\nPlease complete behavioral questionnaires", noWait=True, time=3) # 3 seconds

endTime = time.time()
now = globalClock.getTime()
print("Real time was %0.3f and global clock counted %0.3f (compare %0.6f to initial timing offset to determine drift)" %
      (endTime-startTime, now, now - (endTime-startTime)))

win.close()
core.quit()


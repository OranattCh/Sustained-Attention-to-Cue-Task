# Sustained Attention to Cue Task (SACT)
> Framework to perform cognitive task assessment synchronised with EEG signal recording. Requires [PsychoPy](http://www.psychopy.org/) and [Cognionics - CGX Acquisition](https://www.cgxsystems.com/software).

**Sustained Attention to Cue Task (SACT)** is an accuracy-based version of the psychomotor vigilance task. In this task, participants needed to sustain their attention on a visual circle cue presented at random locations on the screen and ultimately identify a target letter presented briefly at the centre of the cue.

The experimental study is separated into 2 sessions: practice and experiment session. By default setting, the total time of one study is approximately 15 minutes.

**Practice session** will allow participants to be familiar with the task and understand its protocol. The total number of trails is 10 by default. As it is for training, the data will not be saved, and participants will receive feedback about the correctness of their responses. 

**Experiment session** will run in a total of 64 trials with no feedback and no break time. The data will be saved in an Excel sheet and overwritten if there is an existing file.

**Note:** 

* Practice sessions can be skipped or terminated at any time by pressing `escape` key.
* **At this moment, the experiment session cannot be terminated. When you decide to start the study, please note that you will need to perform until the end.**

## Key Files

**Python scripts**

* `main_SACT_exp.py` main code for performing SACT study
* `main_SACT_fn.py` code contains SACT study parameter and protocol

**Images**

* `cue.png`
* `Masked.bmp`
* `cue_B.jpg` `cue_D.jpg` `cue_P.jpg` `cue_R.jpg`
* `target_B.jpg` `target_D.jpg` `target_P.jpg` `target_R.jpg`

**Beep sound**

* `prebeep8bit.wav`

## Requirements

### Python Libraries
![](https://img.shields.io/badge/Tool-NumPy-informational?style=flat&logo=numpy&logoColor=white&color=orange)
![](https://img.shields.io/badge/Tool-Pandas-informational?style=flat&logo=Pandas&logoColor=white&color=orange)
![](https://img.shields.io/badge/Tool-Random-informational?style=flat&logo=Random&logoColor=white&color=orange)
![](https://img.shields.io/badge/Tool-sys-informational?style=flat&logo=sys&logoColor=white&color=orange)
![](https://img.shields.io/badge/Tool-time-informational?style=flat&logo=time&logoColor=white&color=orange)
![](https://img.shields.io/badge/Tool-Parallel-informational?style=flat&logo=parallel&logoColor=white&color=orange)

### Pre-requisite Actions

Make sure that all `parallel` is **not marked as comments**.

To be done in `main_SACT_exp.py`

- Define **location** of source code and data storage: `sys.path.append` and `exp_location`
- Define **window size** in pixels [x, y]: `winsize`
    - Default = [1920,1080]
    - Other options = [1280,720] [1024,768]

To be done in `main_SACT_fn.py`

- Define **number of trials** for both practice and experiment session: `maxrun`
    - Default trial number for practice session is 10
    - Default trial number for experiment session is 64
- **Calibrate mouse position** for each target button
    - Recommended easy way: set `maxrun=8` in `fullexperiment()`. Start the tasks, and click at the lower left and upper right corner of each target.
```
function: _oneProcedure()
variables: resp_x, resp_y
```

| winsize    | target    | resp_x         | resp_y         |
| :---:      | :---:     | :---:          | :---:          |
| [1024, 768]| B         | [-1.29, -1.04] | [-0.63, -0.37] |
|            | D         | [-0.97, -0.72] | [-0.63, -0.37] |
|            | P         | [-0.61, -0.36] | [-0.63, -0.37] |
|            | R         | [-0.29, -0.04] | [-0.63, -0.37] |

| winsize    | target    | resp_x         | resp_y         |
| :---:      | :---:     | :---:          | :---:          |
| [1280, 720]| B         | [-1.51, -1.26] | [-0.63, -0.37] |
|            | D         | [-1.19, -0.94] | [-0.63, -0.37] |
|            | P         | [-0.83, -0.58] | [-0.63, -0.37] |
|            | R         | [-0.51, -0.26] | [-0.63, -0.37] |

| winsize    | target    | resp_x          | resp_y          |
| :---:      | :---:     | :---:           | :---:           |
| [1920,1080]| B         | [-0.63, -0.375] | [-0.125, 0.125] |
|            | D         | [-0.31, -0.06]  | [-0.125, 0.125] |
|            | P         | [0.05, 0.3]     | [-0.125, 0.125] |
|            | R         | [0.37, 0.62]    | [-0.125, 0.125] |

## SACT Output Data

Saved file name is in `SACT_Sxx_Pyy.xlsx` format. `xx` is session, and `yy` is participant code. The format can be changed in `par_info` in `main_SACT_exp.py`.

* `index` index of the procedure, [0-128] combination
* `trial` trial order
* `fix_duration` [2, 3] s
* `cue_duration` [2, 4, 8, 12] s
* `cue_location` [1] topL, [2] topR, [3] bottomL, [4] bottomR
* `target` [1] B, [2] D, [3] P, [4] R  
* `t0` starting time
* `d1` fix_sign time (2, 3 s)
* `d2` beep time (300 ms)
* `d3` dynamic cue time (1500 ms)
* `d4` cue time (2, 4, 8, 12 s)
* `d5` distraction time - on (100 ms)
* `d6` distraction time - off (100 ms)
* `d7` distraction time - on (100 ms)
* `d8` target time (125 ms)
* `d9` target mask time (1 s)
* `rt` reaction time
* `tf` total trial time
* `resp_x, resp_y` mouse click position
* `accuracy` [1] correct response, [0] incorrect
* `response` [1] response received, [0] no response

## EEG Signal Acquisition

* `Trigger #0` start study
* `Trigger #1` start practice session
* `Trigger #2` start experiment session
* `Trigger #100` fixation sign appears on screen
* `Trigger #101` cue appears on screen
* `Trigger #102` distraction sign appears on screen
* `Trigger #103` participant attempts response

## References

Draheim, C., Tsukahara, J. S., Martin, J. D., Mashburn, C. A., & Engle, R. W. (2021). A toolbox approach to improving the measurement of attention control. Journal of Experimental Psychology: General, 150(2), 242.

**Resources:**
```
https://englelab.gatech.edu/attentioncontroltasks
https://englelab.gatech.edu/taskdemos

https://www.youtube.com/watch?v=R4BHsW4OIw8&ab_channel=JasonOzubko
```

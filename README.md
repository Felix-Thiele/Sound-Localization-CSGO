# CSGO Step Sound Localisation

This project aims to detect the direction of incoming sound produced by footsteps in the game CSGO.


We can differentiate between ITD and ILD(IID): timing differences and level(intensity) differences, in the two stereo 
 channels. Csgo seems to only use level differences...

Beware, stereo channels are not sufficient for localization. This code always guesses the 
frontmost possible angle.

## Example of overlay showing detected direction
<img src="https://github.com/Felix-Thiele/Sound-Localization-CSGO/blob/master/extra/csgoimage.JPG" width=100% height=100%>

## Contents and TODO
### Functions to record csgo sounds, and corresponding angles.
   - I used the map https://steamcommunity.com/sharedfiles/filedetails/?id=697998669&searchtext=sound to record sounds. 
### An Overlay to show steps 
   - Streams an overlay onto the screen showing steps, and direction of steps. See the picture above.
### Code to calculate directions
   - There is a high correlation between the rotated degrees and the quotient of the mean values of both channels 
   (see Observation.ipynb).
 - When there are multiple sounds overlapping, this does not yet work. 
   - Problematic on maps with backround noises.
     - Currently I am using band-pass and threshold filtera, better noise cancelation algorithms or filters would be usefull here.
     - Also we could use a better filter to detect step sounds, than the basic threshold algorithm used to determine when to start listeing.
   - Problematic when there are many steps.
     - Steps that already have been detected are not kept in mind, when calculating directions of new steps. This makes 
     the algorithm a bit hit or miss when there are many steps.


### Future?
 - Stereo sound is not sufficient to localize sounds. 
   - Can we calculate together multiple steps, and tracked mouse movements for more precise localisation?
 - Can we also make distance predictions?
   - We might need to take into account some map details, as different surfaces make different step sounds...


## Example for the sound of a step in both channels
![Alt text](extra/csgosound.jpg?raw=true)
## Example for the fourier transform of sound of a step in both channels
![Alt text](extra/csgofourier.jpg?raw=true)

## Interesting Stuff to read:
 - General
  - https://en.wikipedia.org/wiki/Sound_localization
  - https://arxiv.org/pdf/2204.12489.pdf
  - https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=94f2669a3efa6c53003e9eea11b855ea90a7dccf
  - https://www.tu-ilmenau.de/fileadmin/Bereiche/EI/mt-ams/alle_dokumente/manual-robot-control-with-stereo-mic/Final_Thesis_Presentation.pdf
  - https://www.cs.cmu.edu/~robust/Papers/SternWangBrownChapter.pdf
  - https://asa.scitation.org/doi/10.1121/10.0004261
  - https://github.com/shvdiwnkozbw/Multi-Source-Sound-Localization
  - https://github.com/sgraetzer/Akeroyd_parametricilds

 - GCC PHAT
 - https://dsp.stackexchange.com/questions/74574/understanding-gcc-phat-as-a-feature

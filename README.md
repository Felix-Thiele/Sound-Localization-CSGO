# CSGO Step Sound Localisation

This project aims to detect the direction of incoming sound produced by footsteps in the game CSGO.


We can differentiate between ITD and ILD(IID), timing differences and level(intensity) differences in the two stereo 
 channels. Csgo seams to only use level differences...

![Alt text](extra/csgoimage.jpg?raw=true)

## Contents and TODO
### Functions to record csgo sounds, and also the angles from where they came.
   - I used the map https://steamcommunity.com/sharedfiles/filedetails/?id=697998669&searchtext=sound to record sounds. 
### An Overlay to show steps 
    - See the picture above.
### Code to calculate directions
   - There is a high correlation between the rotated degrees and the quotient of the mean values of both channels 
   (see Observation.ipynb). This seems to work pretty well in the isolated environment (e.g. the map mentioned above).
 - When there are multiple sounds overlapping, this does not yet work. 
   - Problematic on maps with backround noises (almost all maps have backround noise at least in certain areas).
   - Problematic when there are many steps.
### Listener for steps
   - Right now we just start listening for steps after a volume threshhold is reached.
     - Can we build better filters for this?
 


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

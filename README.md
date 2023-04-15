# CSGO Step Sound Localisation

This project aims to detect the direction of incoming sound produced by footsteps in the game CSGO.

## Contents
 - Functions to record csgo sounds, and also the angles from where they came.
   - I used the map https://steamcommunity.com/sharedfiles/filedetails/?id=697998669&searchtext=sound to record sounds
 - #TODO Working on code to calculate locations
   - There is a correlation between the rotated degrees and the quotient of the mean values of both channels.


## Observations:
We can differentiate between ITD and ILD(IID), timing differences and level(intensity) differences in the two stereo 
 channels. Csgo seams to only use level differences...
### Example for the sound of a step in both channels
![Alt text](extra/csgosound.jpg?raw=true)
### Example for the fourier transform of sound of a step in both channels
![Alt text](extra/csgofourier.jpg?raw=true)

## Interesting stuff to read:
  - https://github.com/sgraetzer/Akeroyd_parametricilds
  - https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=94f2669a3efa6c53003e9eea11b855ea90a7dccf
  - https://github.com/shvdiwnkozbw/Multi-Source-Sound-Localization
  - https://www.tu-ilmenau.de/fileadmin/Bereiche/EI/mt-ams/alle_dokumente/manual-robot-control-with-stereo-mic/Final_Thesis_Presentation.pdf
  - https://en.wikipedia.org/wiki/Sound_localization
  - https://www.cs.cmu.edu/~robust/Papers/SternWangBrownChapter.pdf
  - https://arxiv.org/pdf/2204.12489.pdf
  - https://asa.scitation.org/doi/10.1121/10.0004261

 - GCC PHAT
    - https://dsp.stackexchange.com/questions/74574/understanding-gcc-phat-as-a-feature

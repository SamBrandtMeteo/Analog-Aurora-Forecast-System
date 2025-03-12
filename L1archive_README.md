L1archive.csv is a file I created that serves as the backbone of this project.
You must provide the script AAFS.py a location to access the file in order for
it to work.

It contains 8 columns:

1) Year:
The year of the L1 observations.
3) Month:
The month of the L1 observations.
4) Day:
The day of the L1 observations.
5) BeginHour:
In UTC; the hour that marks the end of the 1 hour averaging period for solar wind and Bz,
and the beginning of the subsequent 3 hour period over which Kp was measured.
6) Vp:
The bulk proton speed of the solar wind at L1 in units of kilometers per second.
7) Dp:
The density of the protons at L1 in units of protons per cubic centimeter.
8) Bz:
The z-component of the interplanetary magentic field at L1 in units of nanoTeslas.
9) Kp3:
The observed finalized Kp index from GFZ (https://www.gfz.de/en/) for the three hour
period beginning at BeginHour.

If you look through the file, you'll eventually notice some data points that should be
there are missing. This is intentional, as during those times some or all of the required
data from the satellites was either flagged as subpar or missing entirely. 

Despite not being necessary for the specific application of AAFS.py, the proton density
is still included for anyone that wants to perform their own research using the dataset
(perhaps using a machine learning method to improve upon my methodology?)

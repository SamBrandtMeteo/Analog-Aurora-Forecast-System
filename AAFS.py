###############################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

###############################################################################

"""

Inputs
------
path: str
    The path to the location of the L1archive.csv on your machine or 
    cloud-based system of choice. Basically you need to explicitly tell the 
    code where you put the file.
solarwind: str, int, or float
    The current solar wind in units of km/s, averaged over the past 1 hour. For
    manual input, enter an int or float. For the latest data from the DSCOVR
    satellite, enter the str 'latest'.
bz: str, int, or float
    The current IMF Bz component in units of nT, averaged over the past 1 hour.
    For manual input, enter an int or float. For the latest data from the
    DSCOVR satellite, enter the str 'latest'.
    
"""

path='/Users/sxb1072/Desktop/DSCOVRarchive/'

solarwind='latest'

bz='latest'

###############################################################################

def fetch_json(url):
    
    """

    Function that retrieves a json file from a url

    """
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"ERROR: Failed to fetch data from {url}")
        return None
    
def process_json(data):
    
    """
    
    Function that processes data from a json request into a pandas dataframe

    """
    
    df = pd.DataFrame(data)
    df['time_tag'] = pd.to_datetime(df['time_tag'])
    df.set_index('time_tag', inplace=True)
    return df

def pdf(solarwind,bz):
    
    """
    
    Function that calculates the probability distribution function of the
    100 closest points in historical dataset to current solar wind and Bz

    Parameters
    ----------
    solarwind: int or float
        The current bulk solar wind speed in kilometers per second, preferrably 
        averaged over the previous hour.
    bz: int or float
        The current IMF Bz in nanoTeslas, preferrably averaged over the
        previous hour.

    Returns
    -------
    pdf: np.array
        Array containing the Kp values corresponding to the 100 closest points
        in solar wind/Bz space to current conditions.
        
    Calculating Distance
    --------------------
    Calculating distance in this case is non-trivial, since the x and y-axes do
    not share the same units. Therefore, each variable has to be 
    non-dimensionalized before calculating the Euclidean distance. There are a
    couple ways one could go about this. I chose the simple method of dividing
    by the range of the datasets. Solar wind values are non-dimensionalized by
    dividing by 1000 km/s, the approximate range of the dataset, and likewise
    Bz values are divided by 100 nT.
    
    Sample Size
    -----------
    N=100 was chosen mainly because the counts in each bin of the histogram
    will conveniently correspond to probability in the form of percent. It also
    has the benefit of being in a "sweet spot" where the number of samples is
    large enough to produce a realistic looking natural distribution, yet small
    enough to ensure that only points with very similar space weather
    conditions are chosen
    
    """
    
    N=100
    dist=np.sqrt(((solarwind-Vp)/1000)**2+((bz-Bz)/100)**2)
    pdf=Kp3[np.argsort(dist)[:N]]
    
    return pdf

###############################################################################

starlab='manual input'
rtsw_url='https://services.swpc.noaa.gov/json/rtsw/rtsw_'

if type(solarwind)==str or type(bz)==str:
    if solarwind=='latest' or bz=='latest':
        wind=process_json(fetch_json(rtsw_url+'wind_1m.json'))
        mag=process_json(fetch_json(rtsw_url+'mag_1m.json'))
        flag=wind['active']
        solarwind=np.mean(wind['proton_speed'][flag==True][0:60])
        flag=mag['active']
        bz=np.mean(mag['bz_gsm'][flag==True][0:60])
        starlab='last 1 hr avg'
    else:
        print('\n\n\nERROR: Invalid input for variable "solarwind" or "bz"\n\n\n')

###############################################################################

df=pd.read_csv(path+'L1archive.csv')
Bz=np.array(df['Bz'])
Vp=np.array(df['Vp'])
Kp3=np.array(df['Kp3'])

###############################################################################

"""

Filtering
---------
Even after carefully curating this dataset to remove all missing data, some
bad data still remains, mostly in the form of solar wind values erroneously 
clustered around 280 km/s. The test_bool variable is a boolean array that 
removes most of these artificially low solar wind values. In the grand scheme 
of things the number of problematic data points is probably way too small to 
matter for everyday use, but I felt that removing them adds some polish to the 
project. Feel free to comment out the next four lines of code to see what I'm
talking about.

"""

test_bool=~np.logical_and(Kp3>=4,Vp<300)
Vp=Vp[test_bool]
Bz=Bz[test_bool]
Kp3=Kp3[test_bool]

###############################################################################

KpA=pdf(solarwind,bz)

###############################################################################

"""

Scatter Plot Disclaimer
-----------------------
It's important to note that the larger Kp points are plotted with a higher
zorder, so they preferentially appear on top. This was done so that you can
actually see where most of the minor storm conditions are, otherwise most of 
them would be covered up by the vast sea of Kp 1-4 points. That is why I then
made the second probability distribution panel, because it actually shows the 
amount of each Kp surrounding a given solar wind and Bz. I would strongly 
suggest using the left panel to understand the context of the current 
conditions, and using the right panel to actually inform your decisions.

"""

plt.style.use('dark_background')

fig,ax=plt.subplots(nrows=1,ncols=2,dpi=500)

Kp03bool=Kp3<=3.33
Kp4bool=np.logical_and(Kp3>=3.67,Kp3<=4.33)
Kp5bool=np.logical_and(Kp3>=4.67,Kp3<=5.33)
Kp6bool=np.logical_and(Kp3>=5.67,Kp3<=6.33)
Kp7bool=np.logical_and(Kp3>=6.67,Kp3<=7.33)
Kp89bool=Kp3>=7.67

ax[0].scatter(Vp[Kp03bool],Bz[Kp03bool],s=1,c='deepskyblue',label='Kp 0-3',zorder=0)
ax[0].scatter(Vp[Kp4bool],Bz[Kp4bool],s=1,c='lime',label='Kp 4',zorder=0)
ax[0].scatter(Vp[Kp5bool],Bz[Kp5bool],s=1,c='yellow',label='Kp 5 (G1)',zorder=0)
ax[0].scatter(Vp[Kp6bool],Bz[Kp6bool],s=1,c='orange',label='Kp 6 (G2)',zorder=0)
ax[0].scatter(Vp[Kp7bool],Bz[Kp7bool],s=1,c='red',label='Kp 7 (G3)',zorder=0)
ax[0].scatter(Vp[Kp89bool],Bz[Kp89bool],s=1,c='magenta',label='Kp 8-9 (G4-5)',zorder=0)

ax[0].scatter(solarwind,bz,color='black',s=60,zorder=1,marker='*')
ax[0].scatter(solarwind,bz,color='white',s=30,label=starlab,zorder=2,marker='*')

ax[0].legend(fontsize=5.5,loc='lower right')

ax[0].set_xlim(200,1200)
ax[0].set_ylim(-60,40)

ax[0].set_xlabel('Solar Wind Speed ($km$ $s^{-1}$)')
ax[0].set_ylabel('Bz ($nT$)')

ax[0].set_title('Aug 2000 thru Feb 2025 Archive of\nSolar Wind Speed and IMF Bz at L1',fontsize=8)
ax[0].text(220,-59,'GitHub.com/SamBrandtMeteo',fontsize=4,ha='left',va='bottom')

n, bins, patches =ax[1].hist(KpA,bins=np.arange(0,10))
colors = ['deepskyblue','deepskyblue','deepskyblue','deepskyblue','lime','yellow','orange','red','magenta']

for patch, color in zip(patches, colors):
    patch.set_facecolor(color)
    
ax[1].set_xlim(0,9)
if max(n)>50:
    ax[1].set_ylim(0,max(n)+1)
else:
    ax[1].set_ylim(0,50)

ax[1].set_ylabel('Probability (%)')
ax[1].set_xlabel('Kp')

ax[1].set_xticks(np.arange(0,10))

ax[1].set_title('Kp Probabilities over the Next 3 Hours\nBased on 100 Closest Historical Analogs',fontsize=8)

plt.tight_layout()

plt.show()

"""
If you want the code to save the image to your computer,
uncomment the line below and fill in the requisite information.
"""

#plt.savefig('Your/Directory/Here.png')

###############################################################################

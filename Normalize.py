#Normalize the solar radiation flux with the Sun-Earth distance. 
#WMO formula
#Editor: Logothetis Stavros-Andreas

#Libraries
import numpy as np 
import math
import pandas as pd
from datetime import date

#Function that normalize the solar radiation flux

def Normalize(year,month,day,hour,Radiative_Flux):
#day indicates the number of day in the year
    day = (date(year, month, day) - date(year, 1, 1)).days
    E = Radiative_Flux
    delta = year - 1949
    leap = int(delta/4)
    JD = 2432917.5 + delta*365 + leap + day + hour/24
    n = JD - 2451545
    g = 357.528 + 0.9856003*n
    R = 1.00014 - 0.01671*np.cos(g*2*math.pi/360) 
    En = E/R**2
    return(E, En, JD)

df =  pd.read_csv('sbo_Final_2000_present_BSRN_AERONET.csv')
df = df.reset_index()
df.index = pd.to_datetime(df['DateTime'])
df['year'] = df.index.year
df['month'] = df.index.month
df['day'] = df.index.day
df['hour'] = df['Hour'] + df['Minute']*0.01
df.reset_index()

data = []
df.index = df['index']

for i in range(0,len(df)):
    year = df['year'][i]
    month = df['month'][i]
    day = df['day'][i]
    hour = df['hour'][i]
    GHI = df['GHI'][i]
    SF = Normalize(year,month,day,hour,GHI)
    data.append(SF)


columns = ['E','En','JD']
Final_Data = pd.DataFrame(data, columns = columns)
df['GHI_normalize'] = Final_Data['En']
df.to_csv('Normalized.txt')

# ecef_to_eci.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
#   converts ECEF coordinates to ECI coordinates

# Parameters:
#   year: int
#   month: int
#   day: int
#   hour: int
#   minute: int
#   second: float
#   ecef_x_km: x-component of ECEF vector in km
#   ecef_y_km: y-component of ECEF vector in km
#   ecef_z_km: z-component of ECEF vector in km

# Output:
#   ECI coordinates
#
# Written by Grant Chapman
# Other contributors: None

# import Python modules
import sys
import math
import numpy as np

# initialize script arguments
year   = float('nan')
month  = float('nan')
day    = float('nan')
hour   = float('nan')
minute = float('nan')
second = float('nan')
ecef_x_km = float('nan')
ecef_y_km = float('nan')
ecef_z_km = float('nan')

# parse script arguments
if len(sys.argv) == 10:
  year   = int(sys.argv[1])
  month  = int(sys.argv[2])
  day    = int(sys.argv[3])
  hour   = int(sys.argv[4])
  minute = int(sys.argv[5])
  second = float(sys.argv[6])
  ecef_x_km = float(sys.argv[7])
  ecef_y_km = float(sys.argv[8])
  ecef_z_km = float(sys.argv[9])
else:
  print(\
    'Usage: '\
    'python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km'\
  )
  exit()

## script below this line

# julian date
jd = day - 32075 + 1461*(year + 4800 + (month - 14)/12)/4\
+ 367*(month - 2 - (month - 14)/12*12)/12\
- 3*((year + 4900 + (month - 14)/12)/100)/4

# fractional julian date
jd_midnight = int(jd) - 0.5
d_frac = (second + 60*(minute + 60*hour))/86400
jd_frac = jd_midnight + d_frac

# ECEF vector
ecef_vector = [ecef_x_km, ecef_y_km, ecef_z_km]

# getting angle
jd_ut1 = jd_frac
t_ut1 = (jd_ut1 - 2451545.0) / 36525
theta = 67310.54841+(876600*60*60 + 8640184.812866)*t_ut1 + 0.093104*t_ut1**2 - 6.2e-6*t_ut1**3
theta_rad = (theta % 86400)*7.292115e-5

# ecef to eci
r_i_z = [[math.cos(-theta_rad), math.sin(-theta_rad), 0],
         [-math.sin(-theta_rad), math.cos(-theta_rad), 0],
         [0, 0, 1]]

# calculate ecef
eci_vector = np.matmul(r_i_z, ecef_vector)
eci_x_km = eci_vector[0]
eci_y_km = eci_vector[1]
eci_z_km = eci_vector[2]

# print
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)
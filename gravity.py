# -*- coding: utf-8 -*-
"""gravity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10z5EKICTapFrwV-UslSfLrH8pJ22BEEl
"""

!pip install -q condacolab
import condacolab
condacolab.install()

import condacolab
condacolab.check()

!mamba install verde harmonica boule pooch pygmt pyproj pandas xarray

# The standard Python science stack
import numpy as np
import pandas as pd
import xarray as xr
# For projections (wrapped for Proj)
import pyproj
# Plotting maps using GMT
import pygmt
# The Fatiando stack
import pooch
import verde as vd
import boule as bl
import harmonica as hm

url_grav = "https://github.com/yoyo333aaaaa/Latihan/raw/main/ini.csv"
md5_grav = "md5:9e4745a0205871c41fe4f7d6968b97bf"
path_grav = pooch.retrieve(url_grav, known_hash=md5_grav)
print(path_grav)

url_topo = "https://github.com/yoyo333aaaaa/Latihan/raw/main/ini.nc"
md5_topo = "md5:132b2bb514119fa22b2ddb58b0ddbf94"
path_topo = pooch.retrieve(url_topo, known_hash=md5_topo)

data = pd.read_csv(path_grav,names=['longitude','latitude','FAA']).dropna()
data

!pip install netcdf

!pip install xarray
import xarray as xr

topography = xr.load_dataarray(path_topo)
topography

data = pygmt.grdtrack(grid=topography, points=data, newcolname='elevation')
data

fig = pygmt.Figure()
pygmt.makecpt(cmap="seis", series=[data.FAA.min(), data.FAA.max()])
fig.plot(
    x=data.longitude,
    y=data.latitude,
    color=data.FAA,
    cmap=True,
    style="c4p",
    projection="M10c",
    frame=True,
)
fig.coast(resolution='f',shorelines='1p')
fig.colorbar(frame='af+l"FAA [mGal]"')
fig.show()
fig.savefig('FAA.jpg')

fig = pygmt.Figure()
pygmt.makecpt(cmap="earth", series=[topography.values.min(), topography.values.max()])
fig.grdimage(topography, shading=True, projection="M15c", frame=True)
fig.coast(resolution='f',shorelines='1p')
fig.colorbar(frame='af+l"topography [m]"')
fig.show()
fig.savefig('topography.jpg')

topo_plain = vd.project_grid(topography, projection=projection)
topo_plain

bouguer_correction = hm.bouguer_correction(data.elevation)
data["bouguer_corr"] = bouguer_correction
data

data["bouguer_anomaly"] = data.FAA - bouguer_correction
data

fig = pygmt.Figure()
pygmt.makecpt(cmap="seis", series=[data.bouguer_anomaly.min(), data.bouguer_anomaly.max()])
fig.plot(
    x=data.longitude,
    y=data.latitude,
    color=data.bouguer_anomaly,
    cmap=True,
    style="c4p",
    projection="M10c",
    frame=True,
)
fig.coast(resolution='f',shorelines='1p')
fig.colorbar(frame='af+l"simple bouguer anomaly [mGal]"')
fig.show()
fig.savefig('simplebouger_Anomaly.jpg')

coordinates = (data.longitude, data.latitude)
trend = vd.Trend(degree=3).fit(coordinates, data.bouguer_anomaly)

data["regional_anomaly"] = trend.predict(coordinates)
data["residual_anomaly"] = data.bouguer_anomaly - trend.predict(coordinates)
data

fig = pygmt.Figure()
pygmt.makecpt(cmap="seis", series=[data.regional_anomaly.min(), data.regional_anomaly.max()])
fig.plot(
    x=data.longitude,
    y=data.latitude,
    color=data.regional_anomaly,
    cmap=True,
    style="c4p",
    projection="M10c",
    frame=True,
)
fig.coast(resolution='f',shorelines='1p')
fig.colorbar(frame='af+l"regional anomaly [mGal]"')
fig.show()
fig.savefig('regional_Anomaly.jpg')

fig = pygmt.Figure()
pygmt.makecpt(cmap="seis", series=[data.residual_anomaly.min(), data.residual_anomaly.max()])
fig.plot(
    x=data.longitude,
    y=data.latitude,
    color=data.residual_anomaly,
    cmap=True,
    style="c4p",
    projection="M10c",
    frame=True,
)
fig.coast(resolution='f',shorelines='1p')
fig.colorbar(frame='af+l"residual anomaly [mGal]"')
fig.show()
fig.savefig('residual_Anomaly.jpg')

fig.plot(
    x=[110.2974217, 110.3058611, 110.3171136, 110.3262021, 110.336589, 110.3456776, 110.3539006, 110.3653694, 110.3731596, 110.3913367, 110.4237958, 110.4382942, 110.4573369, 110.474432, 110.4859009, 110.4936911],  # Longitude in degrees East
    y=[-8.011843056, -8.000590556, -7.989338083, -7.979600333, -7.966183917, -7.954715028, -7.944328139, -7.92571825, -7.912085444, -7.888065694, -7.855606611, -7.833967222, -7.811029444, -7.790904806, -7.776839222, -7.767967056],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.117179, 110.133928, 110.14096, 110.150678, 110.16132, 110.175293, 110.187809, 110.202193],  # Longitude in degrees East
    y=[-7.624771, -7.630555, -7.63217, -7.633007, -7.634025, -7.635321, -7.636477, -7.637825],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.22952, 110.25365],  # Longitude in degrees East
    y=[-7.69263, -7.69206],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.19054, 110.193665, 110.198213, 110.203131, 110.206194, 110.209535],  # Longitude in degrees East
    y=[-7.71874, -7.719347, -7.720089, -7.719997, -7.719069, -7.717398],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.02453, 110.0347],  # Longitude in degrees East
    y=[-7.60814, -7.60858],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[109.99977, 110.01303, 110.01967],  # Longitude in degrees East
    y=[-7.60991, -7.60902, -7.60858],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.07028, 110.0724, 110.07414, 110.07588, 110.07703, 110.078],  # Longitude in degrees East
    y=[-7.76701, -7.76296, -7.7591, -7.75409, -7.74984, -7.7456],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.06391, 110.05639, 110.05021, 110.04462, 110.04018, 110.03439],  # Longitude in degrees East
    y=[-7.76778, -7.76643, -7.76508, -7.76354, -7.7618, -7.7593],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[109.92431, 109.92351, 109.92272, 109.92192, 109.92139, 109.92059, 109.92050, 109.92050, 109.92024, 109.92077, 109.92074, 109.92058, 109.92042, 109.91962],  # Longitude in degrees East
    y=[-7.58920, -7.59398, -7.59770, -7.60460, -7.60911, -7.61601, -7.62435, -7.62992, -7.63709, -7.64585, -7.64580, -7.65060, -7.65620, -7.66244],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.03404, 110.06248],  # Longitude in degrees East
    y=[-7.77792, -7.78126],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.05864, 110.03335],  # Longitude in degrees East
    y=[-7.79686, -7.80192],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.05720, 110.02395],  # Longitude in degrees East
    y=[-7.80987, -7.81637],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.10995, 110.12296, 110.13958],  # Longitude in degrees East
    y=[-7.81276, -7.83010, -7.85106],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()
fig.savefig('residual_Anomaly.jpg')

fig.plot(
    x=[110.05864, 110.03335],  # Longitude in degrees East
    y=[-7.79686, -7.80192],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()

fig.plot(
    x=[110.05864, 110.03335],  # Longitude in degrees East
    y=[-7.79686, -7.80192],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the survey line
    pen="2p,red",
)
fig.show()
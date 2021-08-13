from pyproj import Proj, transform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from pyproj import Transformer
import dateutil.parser
import pickle
from calendar import monthrange
import datetime
import cartopy.crs as ccrs
import cartopy



def qplot(lon,
          lat,
          data_u,
          data_v,
          bounding_lat=65,
          land=True,
          gridlines=True,
          figsize=[10,5],
          scale=100,
          s=1):
    
    """
    Plots a north polar plot using cartopy. \
    Must be supplied with gridded arrays of lon, lat and data
    """

    
    # Make figure template

    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=ccrs.NorthPolarStereo())

    
    if land == True: # Superimposes a land mask
        ax.add_feature(cartopy.feature.LAND, edgecolor='black',zorder=1)

    # Set the extent of the plot, using the latitudinal limit given in the function arguments    
    
    ax.set_extent([-180, 180, 90, 70], ccrs.PlateCarree())
    
    if gridlines == True:
        ax.gridlines()

    data_u = data_u[::s,::s]
    data_v = data_v[::s,::s]

    
    q = ax.quiver(lon[::s,::s], lat[::s,::s], data_u, data_v,
              transform=ccrs.PlateCarree(),
              scale=scale,
             )
    
    q.set_UVC(data_u,data_v)
    
    plt.show()

def get_month_start_end_doy(month,year):
    
    start_of_month = datetime.date(year=year,month=month,day=1)
    
    start_doy = start_of_month.timetuple().tm_yday
    
    days_in_month = monthrange(year,month)[-1]
    
    end_doy = start_doy + days_in_month
    
    return (start_doy, end_doy)
    

def lonlat_to_xy(coords_1, coords_2, hemisphere, inverse=False):

 

    """Converts between longitude/latitude and EASE xy coordinates.

 

    Args:
        lon (float): WGS84 longitude
        lat (float): WGS84 latitude
        hemisphere (string): 'n' or 's'
        inverse (bool): if true, converts xy to lon/lat

 

    Returns:
        tuple: pair of xy or lon/lat values
    """

 

    EASE_Proj = {'n': 'epsg:3408',
                 's': 'epsg:3409'}
    
    WGS_Proj = 'epsg:4326'
    
    for coords in [coords_1, coords_2]: assert isinstance(coords,(np.ndarray,list))

    if inverse == False: # lonlat to xy
        
        lon, lat = coords_1, coords_2
        
        transformer = Transformer.from_crs(WGS_Proj, EASE_Proj[hemisphere])
        
        x, y = transformer.transform(lat, lon)
        
        return (x, y)

    else: # xy to lonlat
        
        x, y = coords_1, coords_2
        
        transformer = Transformer.from_crs(EASE_Proj[hemisphere], WGS_Proj)
        
        lat, lon = transformer.transform(x, y)
        
        return (lon, lat)

def plot(lon,
          lat,
          data,
          bounding_lat=65,
          land=True,
          gridlines=True,
          figsize=[10,5],
          color_scale=(None,None),
          color_scheme='plasma',
          scale=100):
    
    """
    Plots a north polar plot using cartopy. \
    Must be supplied with gridded arrays of lon, lat and data
    """

    
    # Make figure template

    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=ccrs.NorthPolarStereo())

    
    if land == True: # Superimposes a land mask
        ax.add_feature(cartopy.feature.LAND, edgecolor='black',zorder=1)

    # Set the extent of the plot, using the latitudinal limit given in the function arguments    
    
    ax.set_extent([-180, 180, 90, 70], ccrs.PlateCarree())
    
    if gridlines == True:
        ax.gridlines()
        
    vmin, vmax = color_scale[0], color_scale[1]
    
    c = ax.pcolormesh(lon, lat, data[:,:],
                      transform=ccrs.PlateCarree(),
                      vmin=vmin, vmax=vmax,
                      cmap=color_scheme,
             )
    plt.colorbar(c)
    
    plt.show()


    


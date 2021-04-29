#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists('output'): os.makedirs('output')
# import developed functions
import MyFunctions_RasterExc as funcs


# extract the AOI geometry from OSM
# It is worth noting that 'AOI' should be replaced with a placename present on OpenStreetMap
PlaceGDF = funcs.GeocodePlacenameToGDF('AOI', '28992')

# extract extent from the AOI geometry
bboxAOI = list(PlaceGDF.total_bounds)

# download AHN2 data with 5 meter resolution for the area of interest
DTM = funcs.AHN2_5m_forStudyArea(bboxAOI, './data/AHN2_5m_DTM.tif')

# reclassifies DTM to flooded and dry areas with given waterheight
FloodMap = funcs.CalcFloodMap(DTM, 10, './output/FloodMap.tif')

# Calculate percentage of AOI that will be flooded
import numpy as np
arr = FloodMap.read()
MaxWaterDepth = np.nanmax(arr)
AverageWaterDepth = np.nanmean(arr)
PercWaterCoverage = np.count_nonzero(~np.isnan(arr)) / arr.size *100

from rasterio.plot import show
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,10))
#dsmplot = ax.imshow(FM.read(1), cmap='Oranges', extent=bboxAOI)
show(FloodMap, ax=ax, cmap='Oranges', extent=bboxAOI)
PlaceGDF.plot(ax=ax, color='none', edgecolor='black')
ax.set_title("Waterdepht for flood-case AOI - 10m NAP", fontsize=14)
plt.show()

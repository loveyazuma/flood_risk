#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def GeocodePlacenameToGDF(placename='AOI', EPSGcode='28992'):
    """This function uses the OSMNX package to extract a geometry 
    representing the placename provided as input and transforms to 
    the required projection (EPSG code)"""
    import osmnx as ox
    PlaceGDF = ox.gdf_from_place(placename)
        
    # check first whether there is any output to return
    if len(PlaceGDF) == 1:
        # project GDFs to the required projection
        crs = 'epsg:'+EPSGcode
        try: PlaceGDF = PlaceGDF.to_crs({'init': crs})
        except: print("Given EPSG-code doesn't exist")
        else: return PlaceGDF
    else:
        print("We're sorry, but the given placename is not found within OpenStreetMap. Check for typos or try another placename")


# extract elevation (DTM, DSM and CHM) data for given extent
def AHN2_5m_forStudyArea(bbox, outputfilename):
    
    # load necessary modules
    from owslib.wcs import WebCoverageService
    import rasterio
    
    #specify the AHN3 wcs-url
    wcs = WebCoverageService('http://geodata.nationaalgeoregister.nl/ahn2/wcs?service=WCS', version='1.0.0')

    # Download and save DTM
    response = wcs.getCoverage(identifier='ahn2_5m', bbox=bbox, format='GEOTIFF_FLOAT32',
                               crs='urn:ogc:def:crs:EPSG::28992', resx=5, resy=5)
    with open(outputfilename, 'wb') as file:
        file.write(response.read())

    # Load DTM 
    DTM = rasterio.open(outputfilename, driver="GTiff")
    return DTM

def CalcFloodMap(DEM, waterheight, outputfilename):
    """Function that takes a DEM and waterheight as input, both with same height 
    reference. Output is a reclassificaiton of the input DEM raster specifying 
    whether a cell is flooded, and if so the waterdepth."""
    import rasterio
    rast = DEM.read()
    rast[rast==0] = None
    flood = rast-waterheight
    flood[flood > 0.0] = None
    flood = flood * -1
    kwargs = DEM.meta
    with rasterio.open(outputfilename, 'w', **kwargs) as file:
        file.write(flood.astype(rasterio.float32))
    flood = rasterio.open(outputfilename, driver="GTiff")
    
    return flood

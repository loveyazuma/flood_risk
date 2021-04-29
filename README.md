# Flood Risk
This project aims to calculate areas at risk of flooding.

### Details
* The folder works with a project structure and well-structured scripts were created with one main script. A main.py module was made that imports functions from another Python module called 'MyFunctions_3.py'. 
* The OpenStreetMap data was utilized. The OSMNX package developed by [Geoff Boeing](https://geoffboeing.com/), was employed and the documentation can be found here; [osmnx documentation](https://osmnx.readthedocs.io/en/stable/osmnx.html).

### Processes
- MyFunctions_RasterExc.py was written and three functions to extract the AOI, elevation data and calculate flood map were defined
- A main script was created where the functions from MyFunctions_RasterExc.py were imported
- The Flood map area was visualized with the matplotlib library
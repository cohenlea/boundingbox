# boundingbox
extract bounding box coordinates from a folder of shapefiles and output geojsons and results in a text file

##### install ogr2ogr
brew install GDAL

##### move _coords.py script into shapefile folder

##### create empty _jsons folder inside shapefile folder

##### execute script from folder with shapefiles

#### Note:
- to re run script, delete contents of _jsons folder

- script will check for and delete existing _boundingbox_output.txt file

- works with point, polygon, or multipolygon geometry types
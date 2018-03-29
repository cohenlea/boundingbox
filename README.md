# boundingbox
extract bounding box coordinates from a folder of shapefiles and output geojsons and results in a text file

#### make sure ogr2ogr is installed (brew install GDAL)
#### put _coords.py script into shapefile folder
#### create empty _jsons folder inside shapefile folder
#### need to delete contents of _jsons folder in order to re-run script
#### script will check for and delete existing _boundingbox_output.txt file
#### script only works with point, polygon, or multipolygon geometry types
#### execute script from folder with shapefiles

# shapefiles --> geojsons --> min/max lat/lon bounding box coordinates - loops through folder of shapefiles
# Lea Cohen -- September 2016

# make sure ogr2ogr is installed (brew install GDAL)
# put _coords.py script into shapefile folder
# create empty _jsons folder inside shapefile folder
# need to delete contents of _jsons folder in order to re-run script
# script will check for and delete existing _boundingbox_output.txt file
# script only works with point, polygon, or multipolygon geometry types
# execute script from folder with shapefiles

import json, sys, os, glob, subprocess

o_file = sys.argv[1]	# output text file
try:
	os.remove(o_file)
except OSError as ex:
	print "creating new output file..."

json_folder = "_jsons/"	# folder inside shapefile folder where the output geojsons will be created

for shapefile in glob.glob('*.shp'):
	proc = subprocess.Popen("ogr2ogr -f 'GeoJSON' -t_srs crs:84 " + json_folder + os.path.splitext(shapefile)[0] + ".geojson %s" % (shapefile), shell=True)
	proc.wait()

	inputfile = os.path.splitext(shapefile)[0]+".geojson"
	i_file = json_folder + "%s" % inputfile

	with open(i_file, 'r') as f:
		with open(o_file, 'a') as outputfile:
			data = json.load(f)
			
			minlat = 90
			maxlat = -90
			minlon = 180
			maxlon = -180

			def get_coords(input_pair,min_and_max):
				lon = input_pair[0]
				lat = input_pair[1]

				min_lat = min_and_max[0]
				max_lat = min_and_max[1]
				min_lon = min_and_max[2]
				max_lon = min_and_max[3]

				if lat < min_lat : min_lat = lat
				if lat > max_lat : max_lat = lat
				if lon < min_lon : min_lon = lon
				if lon > max_lon : max_lon = lon
				return (min_lat, max_lat, min_lon, max_lon)

			for feature in data['features']:
				geom_type = feature['geometry']['type']
				if geom_type == "Point":
					feat_coords = feature['geometry']['coordinates']
					(minlat,maxlat,minlon,maxlon) = get_coords(feat_coords,(minlat,maxlat,minlon,maxlon))
				elif geom_type == "Polygon":
					feat_coords = feature['geometry']['coordinates'][0]
					for pair in feat_coords:
						(minlat,maxlat,minlon,maxlon) = get_coords(pair,(minlat,maxlat,minlon,maxlon))
				elif geom_type == "MultiPolygon":
					feat_coords = feature['geometry']['coordinates'][0][0]
					for pair in feat_coords:
						(minlat,maxlat,minlon,maxlon) = get_coords(pair,(minlat,maxlat,minlon,maxlon))
				else:
					print "This script only works with Point, Polygon, or MultiPolygon geometry types."

			a = str(os.path.splitext(inputfile)[0]) + "\n"
			d = "ymin: " + str(minlat) + "\n"
			e = "ymax: " + str(maxlat) + "\n"
			b = "xmin: " + str(minlon) + "\n"
			c = "xmax: " + str(maxlon) + "\n"

			outputfile.write(a+b+c+d+e+"\n")


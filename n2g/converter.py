#!/usr/bin/python3

from PyNotam import notam
from geojson import FeatureCollection, Feature, Polygon
from shapely.geometry.point import Point
from shapely.ops import transform
from functools import partial
import numpy as np
import pyproj
import geojson
import re

class n2g:

    def __init__(self, notams):
        self.notams = notams

    def from_cord_to_dd(self, lat, lon):
            sig = -1 if re.search('[swSW]', lat) else 1
            if len(lat) <= 5:
                lat = sig * (int(lat[:-3]) + float(lat[2:-1]) / 60)
            else:
                lat = sig * (int(lat[:-5]) + float(lat[2:-3]) / 60 + float(lat[4:-1]) / 360)

            sig = -1 if re.search('[swSW]', lon) else 1
            if len(lon) <= 6:
                lon = sig * (int(lon[:-3]) + float(lon[2:-1]) / 60)
            else:
                lon = sig * (int(lon[:-5]) + float(lon[2:-3]) / 60 + float(lon[4:-1]) / 360)
            return lat, lon


    def to_geojson(self):
        polygons = []
        for n in self.notams:
            decoded = notam.Notam.from_str(n)

            area = decoded.area
            lat = area["lat"]
            lon = area["long"]

            lat, lon = self.from_cord_to_dd(lat, lon)

            radius = area["radius"] # in nautical miles. WHAT THE FUCK Y U NO UZE METRIC
            radius *= 1852; # this is the really dumb simple way to get to meters
            # I have now discovered that _some_ (not all) NOTAMS explicitly note that they are using km.
            # this fucking format, I tell you
            local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon)

            wgs84_to_aeqd = partial(
                pyproj.transform,
                pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
                pyproj.Proj(local_azimuthal_projection),
            )
            aeqd_to_wgs84 = partial(
                pyproj.transform,
                pyproj.Proj(local_azimuthal_projection),
                pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
            )


            center = Point(float(lon), float(lat))
            point_transformed = transform(wgs84_to_aeqd, center)
            buffer = point_transformed.buffer(radius)

            circle = []
            for x, y in transform(aeqd_to_wgs84, buffer).exterior.coords:
                circle.append([x, y])

            polygons.append(Feature(geometry=Polygon([circle]),
                properties={"title":str(decoded.notam_id), "description":str(decoded.purpose)}))


            poly = []
            if decoded.poly is not None:
                for point in decoded.poly:

                    poly.append(self.from_cord_to_dd(point["long"], point["lat"])) # I don't know why these are backwards. But it seems to work

                polygons.append(Feature(geometry=Polygon([poly]),
                    properties={"title":str(decoded.notam_id), "description":str(decoded.indices_item_e)}))

                #np.append([polygons], [Feature(geometry=Polygon([poly]),
                #    properties={"title":str(decoded.notam_id), "description":str(decoded.indices_item_e)})]).tolist()


            # decoded.area is only determined from q-clause
            # there is often more detail in the e clause (search for "AREA")
            # but those are somewhat unstructured
            # TODO: add the capability to handle those coords

        return geojson.dumps(FeatureCollection(polygons))

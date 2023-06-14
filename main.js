import "./style.css";
import { Map, View } from "ol";
import TileLayer from "ol/layer/Tile";
import GeoTIFF from "ol/source/GeoTIFF.js";
import OSM from "ol/source/OSM";
import { Vector as VectorLayer } from "ol/layer";
import { Vector as VectorSource } from "ol/source";
import ImageLayer from "ol/layer/Image";
import ImageStatic from "ol/source/ImageStatic";
import { getCenter } from "ol/extent";
import proj4 from 'proj4';
import {applyTransform} from 'ol/extent.js';
import {get as getProjection, getTransform} from 'ol/proj.js';
import {register} from 'ol/proj/proj4.js';
import {transformExtent} from 'ol/proj';

// Create a vector source and layer for drawing
const vectorSource = new VectorSource({
  wrapX: false,
});
const editLayer = new VectorLayer({
  source: vectorSource,
});

const map = new Map({
  target: "map",
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
    editLayer, // Add the vector layer to the map
  ],
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
});

var editor = new ole.Editor(map);

var cad = new ole.control.CAD({
  source: editLayer.getSource(),
});

var draw = new ole.control.Draw({
  source: editLayer.getSource(),
});

var drawLine = new ole.control.Draw({
  type: 'LineString',
  source: editLayer.getSource(),
});

var drawPoly = new ole.control.Draw({
  type: 'Polygon',
  source: editLayer.getSource(),
});

editor.addControls([draw, cad, drawLine, drawPoly]);

// Read TIFF file names and extent from data.json
fetch("data.json")
  .then((response) => response.json())
  .then((data) => {
    const { file_names, min_x, min_y, max_x, max_y } = data;
        // Calculate center and zoom based on the TIFF file extent
        const extent = [min_x, min_y, max_x, max_y];
        // var extent= transformExtent(extent2, 'EPSG:28992', 'EPSG:3857');

    // Create image layers for each TIFF file
    file_names.forEach((file) => {
      const imageLayer = new ImageLayer({
        source: new ImageStatic({
          url: 'data/geotiff_TILE_000_BAND_perc_95_normalized_height.png',
          imageExtent: extent,
        }),
      });
      map.addLayer(imageLayer);
    });


    const center = getCenter(extent);
    const zoom = map.getView().getZoomForResolution(
      map.getView().getResolutionForExtent(extent)
    );

    // Update the view to center the map around the TIFF files
    map.getView().setCenter(center);
    map.getView().setZoom(zoom);
  });

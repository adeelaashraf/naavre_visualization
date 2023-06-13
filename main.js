import "./style.css";
import { Map, View } from "ol";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { Vector as VectorLayer } from "ol/layer";
import { Vector as VectorSource } from "ol/source";
import ImageLayer from "ol/layer/Image";
import ImageStatic from "ol/source/ImageStatic";
import { getCenter } from "ol/extent";

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

    // Create image layers for each TIFF file
    file_names.forEach((file) => {
      const imageLayer = new TileLayer({
        source: new ImageStatic({
          url: file,
          imageExtent: [min_x, min_y, max_x, max_y],
        }),
      });
      map.addLayer(imageLayer);
    });

    // Calculate center and zoom based on the TIFF file extent
    const extent = [min_x, min_y, max_x, max_y];
    const center = getCenter(extent);
    const zoom = map.getView().getZoomForResolution(
      map.getView().getResolutionForExtent(extent)
    );

    // Update the view to center the map around the TIFF files
    map.getView().setCenter(center);
    map.getView().setZoom(zoom);
  });

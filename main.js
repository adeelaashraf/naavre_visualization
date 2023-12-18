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
import {ScaleLine, defaults as defaultControls} from 'ol/control.js';
import {FullScreen, defaults as defaultControls2} from 'ol/control.js';

import data from './data.json'

/*
Sources used:
https://openlayers.org/en/latest/examples/reprojection-by-code.html
https://openlayers.org/en/latest/examples/popup.html
https://openlayers.org/en/latest/examples/projection-and-scale.html
https://openlayers.org/en/latest/examples/full-screen.html
https://github.com/geops/openlayers-editor
*/

const fpsCounter = document.getElementById('fpsCounter');

// Variables for FPS calculation
let frames = 0;
let lastTime = performance.now();
let accumulatedTime = 0;

// Function to update the FPS counter
function updateFPS() {
  const currentTime = performance.now();
  const deltaTime = currentTime - lastTime;
  lastTime = currentTime;

  accumulatedTime += deltaTime;
  frames++;

  // Check if 3 seconds have passed
  if (accumulatedTime >= 1000) {
    const avgFPS = Math.round((frames / (accumulatedTime / 1000)));
    fpsCounter.innerText = `FPS: ${avgFPS}`;
    accumulatedTime = 0;
    frames = 0;
  }

  // Request the next animation frame
  requestAnimationFrame(updateFPS);
}

// Call the updateFPS function to start the FPS counter
updateFPS();



// Create a vector source and layer for drawing
const vectorSource = new VectorSource({
  wrapX: false,
});
const editLayer = new VectorLayer({
  source: vectorSource,
});

const scaleControl = new ScaleLine({
  units: 'metric',
  bar: true,
  steps: 4,
  text: true,
  minWidth: 140,
});


const attributions =
  'Version ' + data.version + ' Developed at ' +
  ' <a href="https://www.uva.nl/" target="_blank"> University of Amsterdam</a>' +
  ' <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>';

const map = new Map({
  controls: defaultControls().extend([scaleControl, new FullScreen()]),
  target: "map",
  layers: [
    new TileLayer({
      source: new OSM({
        attributions: attributions
      }),
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

// Add the data
const pngFiles = data.png_files;

for (const key in pngFiles) {
  if (pngFiles.hasOwnProperty(key)) {
    const file = pngFiles[key];

    const { file_name, min_x, min_y, max_x, max_y } = file;
    const extent = [min_x, min_y, max_x, max_y];

    console.log('File Name:', file_name);
    console.log('min_x:', min_x);
    console.log('min_y:', min_y);
    console.log('max_x:', max_x);
    console.log('max_y:', max_y);

    const imageLayer = new ImageLayer({
      source: new ImageStatic({
        url: file_name,
        imageExtent: extent,
      }),
    });
    map.addLayer(imageLayer);
  }
}

 function setProjection(code, name, proj4def, bbox) {
  if (code === null || name === null || proj4def === null || bbox === null) {
  console.log("here")
    map.setView(
      new View({
        projection: 'EPSG:3857',
        center: [0, 0],
        zoom: 1,
      })
    );
    return;
  }

  const newProjCode = 'EPSG:' + code;
  proj4.defs(newProjCode, proj4def);
  register(proj4);
  const newProj = getProjection(newProjCode);
  const fromLonLat = getTransform('EPSG:4326', newProj);

  let worldExtent = [bbox[1], bbox[2], bbox[3], bbox[0]];
  newProj.setWorldExtent(worldExtent);

  // approximate calculation of projection extent,
  // checking if the world extent crosses the dateline
  if (bbox[1] > bbox[3]) {
    worldExtent = [bbox[1], bbox[2], bbox[3] + 360, bbox[0]];
  }
  const extent = applyTransform(worldExtent, fromLonLat, undefined, 8);
  newProj.setExtent(extent);
  const newView = new View({
    projection: newProj,
  });
  map.setView(newView);
  newView.fit(extent);
}

function search(query) {
  fetch('https://epsg.io/?format=json&q=' + query)
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      const results = json['results'];
      if (results && results.length > 0) {
        for (let i = 0, ii = results.length; i < ii; i++) {
          const result = results[i];
          if (result) {
            const code = result['code'];
            const name = result['name'];
            const proj4def = result['wkt'];
            const bbox = result['bbox'];
            if (
              code &&
              code.length > 0 &&
              proj4def &&
              proj4def.length > 0 &&
              bbox &&
              bbox.length == 4
            ) {
              setProjection(code, name, proj4def, bbox);
              return;
            }
          }
        }
      }
      setProjection(null, null, null, null);
    });
}

search(data.projection)

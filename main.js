import "./style.css";
import * as ol from "ol";
import {Map, View} from "ol";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import {
    DragRotateAndZoom,
    defaults as defaultInteractions,
} from "ol/interaction.js";

const map = new Map({
 interactions: defaultInteractions().extend([new DragRotateAndZoom()]),
  target: "map",
  layers: [
    new TileLayer({
      source: new OSM()
    })
  ],
  view: new View({
    center: [0, 0],
    zoom: 2
  })
});


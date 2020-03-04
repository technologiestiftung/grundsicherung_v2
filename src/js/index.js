import "whatwg-fetch";
import "core-js/stable";
// import "regenerator-runtime/runtime";
import "../css/index.scss";
import { map } from "./map";
import { linechart } from "./linechart";
import { timelapse } from "./timelapse";
import { counter } from "./counter";
import { scroll2top } from "./back2top";

document.addEventListener("DOMContentLoaded", function() {
  map();
  linechart();
  timelapse();
  counter();
  scroll2top();
});

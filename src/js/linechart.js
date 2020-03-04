import { Linechart } from "./Linechart-class";
export function createLineChart() {
  // document.addEventListener("DOMContentLoaded", function() {
  const style = window.getComputedStyle(document.getElementById("intro"), null);
  const padding_total = parseFloat(style["paddingLeft"].replace("px", "")) * 2;
  const width_temp = parseFloat(style["width"]);
  const width = width_temp - padding_total;

  // Line Chart
  var line_config = {
    div: "timeline",
    file: "data/timeline.csv",
    width: width,
    xaxis: "jahr",
    yaxis: "ab 65 Jahre insgesamt",
    line2: "18-64 Jahre insgesamt",
    yunit: "% ",
    ylabel: "% Grundsicherungsempfänger*innen"
  };

  const linechart = new Linechart(line_config).init();
  // });
}

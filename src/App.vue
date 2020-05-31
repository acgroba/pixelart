<template>
  <div id="app">
    <fab
      :position="fabs.showTemplatesButton.position"
      :bg-color="fabs.showTemplatesButton.bgColor"
      :main-icon="'visibility'"
      @click.native="showTemplates"
    ></fab>

    <fab
      :position="fabs.settingsButton.position"
      :bg-color="fabs.settingsButton.bgColor"
      :actions="fabs.settingsButton.fabActions"
      :main-icon="'settings'"
      @clearGrid="clearGrid"
      @save="generateImage"
    ></fab>

    <div class="container" style="display: flex">
      <div id="caroussel">
        <hooper
          v-if="template_active"
          ref="hooper"
          :vertical="true"
          style="height: 100vmin"
          :itemsToShow="5"
          :centerMode="true"
          :infiniteScroll="true"
          @slide="updateTemplate"
        >
          <slide v-for="(template, templateIndex) in templates" :key="templateIndex">
            <img
              @click="changeSlide(templateIndex)"
              class="slide-image"
              :src="getImageSrc(template)"
            />
          </slide>
          <hooper-navigation slot="hooper-addons"></hooper-navigation>
        </hooper>
      </div>
      <div class="grid-container">
        <table>
          <tr v-for="(row, rowIndex) in visibleCells" :key="rowIndex">
            <td
              class="cell"
              :style="{
                width: cellSide,
                height: cellSide,
                'background-color': cell.background
              }"
              v-for="(cell, colIndex) in row"
              :key="colIndex"
              @mousedown="mouseDown(cell)"
              @mouseup="mouseUp(cell)"
              @mouseover="mouseOver(cell)"
            ></td>
          </tr>
        </table>
      </div>

      <div class="palette">
        <swatches v-model="color" :colors="colors" swatch-size="60" inline></swatches>
      </div>
    </div>
  </div>
</template>

<script>
import fab from "vue-fab";
import axios from "axios";
import templates from "@/constants/templates.js";
import Swatches from "vue-swatches";
import "vue-swatches/dist/vue-swatches.min.css";
import { Hooper, Slide } from "hooper";
import { Navigation as HooperNavigation } from "hooper";
import "hooper/dist/hooper.css";

const TOTAL_ROW_CELLS = 50;
const PIXEL_SIZE = 20;
const HTTP = axios.create({
  baseURL: `https://api.mrbroc.com/editor/`
});

export default {
  name: "app",
  components: { fab, Swatches, Hooper, Slide, HooperNavigation },

  data: function() {
    return {
      tiles: [],
      templates: [],
      active_template: 0,
      cellsWindowSide: 20,
      cellsWindowCenterX: 25,
      cellsWindowCenterY: 25,
      clicked: false,
      template_active: false,
      colors: [
        "#e8c2b2",
        "#022d83",
        "#fddf00",
        "#3676b4",
        "#e89702",
        "#75b3d3",
        "#de6c15",
        "#898eb5",
        "#d21920",
        "#66a92d",
        "#dd94bd",
        "#7a8752",
        "#aa86b6",
        "#aac055",
        "#622280",
        "#a2682b",
        "#434544",
        "#717373"
      ],
      fabs: {
        settingsButton: {
          bgColor: "#778899",
          position: "bottom-left",
          fabActions: [
            {
              name: "clearGrid",
              icon: "delete",
              color: "#fe6c61"
            },
            {
              name: "save",
              icon: "save",
              color: " #62caaa"
            }
          ]
        },
        showTemplatesButton: {
          bgColor: "#778899",
          position: "top-left"
        }
      },
      color: "#1CA085"
    };
  },

  computed: {
    cellSide: function() {
      return this.visibleCells[0].length / 100 + "%";
    },

    visibleCells: function() {
      let cells = [];
      let cellsWindowCenterY = parseInt(this.cellsWindowCenterY);
      let cellsWindowCenterX = parseInt(this.cellsWindowCenterX);
      let cellsWindowSide = parseInt(this.cellsWindowSide);
      this.tiles
        .slice(
          cellsWindowCenterY - cellsWindowSide / 2,
          cellsWindowCenterY + cellsWindowSide / 2
        )
        .forEach(row => {
          cells.push(
            row.slice(
              cellsWindowCenterX - cellsWindowSide / 2,
              cellsWindowCenterX + cellsWindowSide / 2
            )
          );
        });
      return cells;
    }
  },
  methods: {
    updateTemplate: function(payload) {
      if (payload.currentSlide >= this.templates.length) {
        this.active_template = 0;
      } else if (payload.currentSlide < 0) {
        this.active_template = this.templates.length - 1;
      } else {
        this.active_template = payload.currentSlide;
      }

      this.clearGrid();
    },
    showTemplates: function() {
      if (!this.template_active) {
        this.template_active = true;

        this.fabs.showTemplatesButton.bgColor = "#a6feee";
      } else {
        this.template_active = false;

        this.fabs.showTemplatesButton.bgColor = "#778899";
        this.clearGrid();
      }
    },
    clearGrid: function() {
      let self = this;

      if (this.template_active) {
        var max = self.getMax(self.templates[self.active_template].numbers) + 1;
        var step = parseInt(256 / max);

        this.cellsWindowSide =
          self.templates[self.active_template].numbers.length;
      }
      let limit =
        this.cellsWindowCenterY - Math.round(this.cellsWindowSide / 2);
      this.tiles = [];
      for (let i = 0; i < TOTAL_ROW_CELLS; i++) {
        let row = [];
        for (let j = 0; j < TOTAL_ROW_CELLS; j++) {
          if (
            this.template_active &&
            i >= limit &&
            j >= limit &&
            i < limit + this.cellsWindowSide &&
            j < limit + this.cellsWindowSide
          ) {
            let number =
              self.templates[self.active_template].numbers[i - limit][
                j - limit
              ] + 1;
            let color =
              (number * step).toString(16) +
              (number * step).toString(16) +
              (number * step).toString(16);
            if (number == max) {
              row.push({
                row: i,
                col: j,
                value: 0,
                background: "#" + color,
                text: "_"
              });
            } else {
              row.push({
                row: i,
                col: j,
                value: 0,
                background: "#" + color,
                text: number
              });
            }
          } else {
            row.push({
              row: i,
              col: j,
              value: 0,
              background: "#FFFFFF",
              text: " "
            });
          }
        }
        this.tiles.push(row);
      }
    },
    generateImageJSON: function() {
      let image = [];
      for (const [i, row] of this.visibleCells.entries()) {
        let row_colors = [];
        for (const [j, cell] of row.entries()) {
          row_colors.push(cell.background);
        }
        image.push(row_colors);
      }
      console.log(JSON.stringify(image));
    },
    generateImage: function() {
      this.$loadScript("/pnglib.js")
        .then(() => {
          var size = this.visibleCells.length * PIXEL_SIZE;
          var p = new PNGlib(size, size, 256); // construcor takes height, weight and color-depth

          for (const [i, row] of this.visibleCells.entries()) {
            for (const [j, cell] of row.entries()) {
              var R = parseInt(cell.background.substring(1, 3), 16);
              var G = parseInt(cell.background.substring(3, 5), 16);
              var B = parseInt(cell.background.substring(5), 16);

              for (var u = 0; u < PIXEL_SIZE; u++) {
                for (var v = 0; v < PIXEL_SIZE; v++) {
                  p.buffer[
                    p.index(j * PIXEL_SIZE + v, i * PIXEL_SIZE + u)
                  ] = p.color(R, G, B);
                }
              }
            }
          }
          var download = document.createElement("a");
          download.href = "data:image/png;base64," + p.getBase64();
          download.download = "pixelart.png";
          download.click();
        })
        .catch(() => {
          // Failed to fetch script
        });
    },

    mouseDown: function(cell) {
      this.cellClick(cell);
      this.clicked = true;
    },
    mouseUp: function() {
      this.clicked = false;
    },
    moveUp: function() {
      if (
        this.cellsWindowCenterY + this.cellsWindowSide < TOTAL_ROW_CELLS &&
        !this.template_active
      ) {
        this.cellsWindowCenterY = this.cellsWindowCenterY + 1;
      }
    },
    moveDown: function() {
      if (
        this.cellsWindowCenterY - this.cellsWindowSide > 0 &&
        !this.template_active
      ) {
        this.cellsWindowCenterY = this.cellsWindowCenterY - 1;
      }
    },
    moveLeft: function() {
      if (!this.template_active) {
        this.cellsWindowCenterX = this.cellsWindowCenterX + 1;
      }
    },
    moveRight: function() {
      if (!this.template_active) {
        this.cellsWindowCenterX = this.cellsWindowCenterX - 1;
      }
    },
    zoomIn: function() {
      if (this.cellsWindowSide > 3 && !this.template_active) {
        this.cellsWindowSide = this.cellsWindowSide - 2;
      }
    },
    zoomOut: function() {
      if (this.cellsWindowSide + 2 < TOTAL_ROW_CELLS && !this.template_active) {
        this.cellsWindowSide = this.cellsWindowSide + 2;
      }
    },
    mouseOver: function(cell) {
      if (this.clicked && cell.background != this.colors) {
        this.cellClick(cell);
      }
    },
    cellClick(cell) {
      if (cell.background != this.color) {
        cell.background = this.color;
      } else {
        cell.background = "#FFFFFF";
      }
    },
    getMax(arr) {
      var maxRow = arr.map(function(row) {
        return Math.max.apply(Math, row);
      });
      return Math.max.apply(null, maxRow);
    },
    getImageSrc: function(template) {
      return require("@/assets/templates/" + template.file);
    },
    changeSlide(slide) {
      this.$refs.hooper.slideTo(slide);
    }
  },
  created() {
    let self = this;
    window.addEventListener("keyup", function(event) {
      if (event.code == "ArrowUp") {
        self.moveUp();
      } else if (event.code == "ArrowDown") {
        self.moveDown();
      } else if (event.code == "ArrowRight") {
        self.moveRight();
      } else if (event.code == "ArrowLeft") {
        self.moveLeft();
      } else if (event.code == "Enter") {
        self.zoomIn();
      } else if (event.code == "Backspace") {
        self.zoomOut();
      }
    });
    self.templates = templates;

    this.clearGrid();
  }
};
</script>

<style>
body {
  margin: 0 !important;
}

.grid-container {
  width: 100vmin;
  height: 100vmin;

  margin-right: calc((100vmax - 100vmin) / 6);
}
.palette {
  height: 100vmin;
}
table {
  -webkit-border-horizontal-spacing: 0;
  -webkit-border-vertical-spacing: 0;
  table-layout: fixed;
  height: 100vmin;
  width: 100vmin;
  font-size: 2vmin;
}

td.cell {
  border: solid;
  border-width: 1px;
  padding: 0;
  text-align: center;
  user-select: none;
}

.container {
  position: relative;
}
#caroussel {
  margin-left: calc((100vmax - 100vmin) / 4);
  margin-right: 2vmin;
}
.slide-image {
  height: 15vmin;
  width: 15vmin;
}
.hooper-slide {
  background-color: #62caaa;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #fff;
  border-radius: 10px;
}
.hooper-slide.is-current {
  transform: scale(1.2);
  background-color: #a6feee;
}
</style>

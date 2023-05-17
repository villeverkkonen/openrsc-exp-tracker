const { createCanvas } = require("canvas");
const canvas = createCanvas(500, 500);
global.HTMLCanvasElement.prototype.getContext = canvas.getContext("2d");

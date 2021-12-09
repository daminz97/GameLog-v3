// draw pie chart
function drawPie() {
    var plotCost = document.getElementById("pie-chart");
    const costs = JSON.parse(document.getElementById('costs').textContent);

    var gamingCost = {
        "Xbox": 0,
        "Steam": 0,
        "Nintendo": 0,
        "PlayStation": 0,
    };
    for (let i in costs) {
        if (costs[i]['platform'] == 'Xbox') {
            gamingCost['Xbox'] = costs[i]['num'];
        } else if (costs[i]['platform'] == 'Steam') {
            gamingCost['Steam'] = costs[i]['num'];
        } else if (costs[i]['platform'] == 'PlayStation') {
            gamingCost['PlayStation'] = costs[i]['num']
        } else {
            gamingCost['Nintendo'] = costs[i]['num']
        }
    }

    function drawPieSlice(ctx, centerX, centerY, radius, startAngle, endAngle, color) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }

    var PieChart = function(options) {
        this.options = options;
        this.canvas = options.canvas;
        this.ctx = this.canvas.getContext("2d");
        this.colors = options.colors;

        this.draw = function() {
            var total_value = 0;
            var color_index = 0;
            for (var categ in this.options.data) {
                var val = this.options.data[categ];
                total_value += val;
            }

            var start_angle = 0;
            for (categ in this.options.data) {
                val = this.options.data[categ];
                var slice_angle = 2 * Math.PI * val / total_value;

                drawPieSlice(
                    this.ctx,
                    this.canvas.width / 2,
                    this.canvas.height / 2,
                    Math.min(this.canvas.width / 2, this.canvas.height / 2),
                    start_angle,
                    start_angle + slice_angle,
                    this.colors[color_index % this.colors.length]
                );

                start_angle += slice_angle;
                color_index += 1;
            }

            if (this.options.legend) {
                color_index = 0;
                var legendHTML = "";
                for (categ in this.options.data) {
                    legendHTML += "<div><span style='display:inline-block;width:20px;background-color:" + this.colors[color_index++] + ";'>&nbsp;</span> " + categ + "</div>";
                }
                this.options.legend.innerHTML = legendHTML;
            }
        }
    }

    var myPieChart = new PieChart({
        canvas: plotCost,
        data: gamingCost,
        colors: ["#cbeabd", "#aec6a5", "#769174", "#b1af96", "#91887b"],
        legend: myLegend
    });
    myPieChart.draw();
}

drawPie();


// draw line chart
function drawGraph() {
    var myCanvas = document.getElementById("bar-chart");
    const times = JSON.parse(document.getElementById('times').textContent);

    months = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 'November', 'December'];
    
    first_month = Object.keys(times)[0];
    last_month = Object.keys(times)[-1];
    for (let i=months.indexOf(first_month); i<months.indexOf(last_month); i++) {
        if (!times.hasOwnProperty(months[i])) {
            times[months[i]] = 0.0;
        }
    };

    function drawLine(ctx, startX, startY, endX, endY, color) {
        ctx.save();
        ctx.strokeStyle = color;
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
        ctx.restore();
    }

    function drawBar(ctx, upperLeftCornerX, upperLeftCornerY, width, height, color) {
        ctx.save();
        ctx.fillStyle = color;
        ctx.fillRect(upperLeftCornerX, upperLeftCornerY, width, height);
        ctx.restore();
    }

    var Barchart = function(options) {
        this.options = options;
        this.canvas = options.canvas;
        this.ctx = this.canvas.getContext('2d');
        this.colors = options.colors;

        this.draw = function() {
            var maxVal = 0;
            for (var categ in this.options.data) {
                maxVal = Math.max(maxVal, this.options.data[categ]);
            }
            var canvasActualHeight = this.canvas.height - this.options.padding * 2;
            var canvasActualWidth = this.canvas.width - this.options.padding * 2;

            var gridVal = 0;
            while (gridVal <= maxVal) {
                var gridY = canvasActualHeight * (1 - gridVal / maxVal) + this.options.padding;
                drawLine(
                    this.ctx,
                    0,
                    gridY,
                    this.canvas.width,
                    gridY,
                    this.options.gridColor
                );

                this.ctx.save();
                this.ctx.fillStyle = this.options.gridColor;
                this.ctx.font = "bold 10px Arial";
                this.ctx.fillText(gridVal, 10, gridY - 2);
                this.ctx.restore();

                gridVal += this.options.gridScale;
            }

            //drawing the bars
            var barIndex = 0;
            var numberOfBars = Object.keys(this.options.data).length;
            var barSize = (canvasActualWidth) / numberOfBars;

            for (categ in this.options.data) {
                var val = this.options.data[categ];
                var barHeight = Math.round(canvasActualHeight * val / maxVal);
                drawBar(
                    this.ctx,
                    this.options.padding + barIndex * barSize,
                    this.canvas.height - barHeight - this.options.padding,
                    barSize,
                    barHeight,
                    this.colors[barIndex % this.colors.length]
                );

                barIndex += 1;
            }

            //draw legend
            barIndex = 0;
            var legend = document.querySelector("legend[for='myCanvas']");
            var ul = document.createElement("ul");
            legend.append(ul);
            for (categ in this.options.data) {
                var li = document.createElement("li");
                li.style.listStyle = "none";
                li.style.borderLeft = "20px solid " + this.colors[barIndex % this.colors.length];
                li.style.padding = "5px";
                li.textContent = categ;
                ul.append(li);
                barIndex++;
            }
        }
    }

    var myBarchart = new Barchart({
        canvas: myCanvas,
        padding: 10,
        gridScale: 5,
        gridColor: "#eeeeee",
        data: times,
        colors: ["#cbeabd", "#aec6a5", "#769174", "#b1af96", "#91887b"]
    });
    myBarchart.draw();
}

drawGraph();

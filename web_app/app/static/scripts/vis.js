
var url_string = window.location.href;
var url = new URL(url_string);
var name = url.searchParams.get("name");
console.log(name);

var model_data;
$.getJSON("/_model_data", {name:name}, function(data){
    model_data = data.out;
    //TODO Add graph plotting stuff

    var width = 420,
    barHeight = 20;

var x = d3.scale.linear()
    .domain([0, d3.max(model_data)])
    .range([0, width]);

var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", barHeight * model_data.length);

var bar = chart.selectAll("g")
    .data(model_data)
    .enter().append("g")
    .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

bar.append("rect")
    .attr("width", x)
    .attr("height", barHeight - 1);

bar.append("text")
    .attr("x", function(d) { return x(d) - 3; })
    .attr("y", barHeight / 2)
    .attr("dy", ".35em")
    .text(function(d) { return d; });

});

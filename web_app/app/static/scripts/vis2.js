
var url_string = window.location.href;
var url = new URL(url_string);
var name = url.searchParams.get("name");
console.log(name);

var model_data;
$(document).ready(function (){

$('#go').on('click', function(){console.log('a')})

$('#go').on('click', function(){
    $.getJSON("/_model_data", {name:$('#name').val()}, function(data){
        model_data = data.out;
        //TODO Add graph plotting stuff
        $("#graphs").empty();
        $("#graphs").append( '<svg width="960" height="500" class="chart"></svg>"');
        var width = 420,
        barHeight = 20;


    var x = d3.scaleLinear()
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

    $.getJSON("/_chat_data", {name:$('#name').val()}, function(data){
        console.log(data)
        chat_data = data.out;
        $("#questions").empty();
        var html = '<h2>Problems</h2><table class="table"><thead><th>Problem</th><th>Severity</th></thead><tbody>';
        console.log(chat_data[0])
        for (var i=0; i<chat_data.length; i++){
            console.log(chat_data[i])
            for (var key in chat_data[i]){
                html+='<tr><td>'+key+'</td><td>'+chat_data[i][key]+'</td></tr>'
            }
        }
        html+='</tbody></table>'
        $('#questions').append(html)
    });
})
})

var url_string = window.location.href;
var url = new URL(url_string);
var name = url.searchParams.get("name");
console.log(name);

var model_data;

var descs = {
0: "Normal",
1:"Ischemic changes (Coronary Artery Disease)",
2:"Old Anterior Myocardial Infarction",
3:"Old Inferior Myocardial Infarction",
4:"Sinus tachycardy",
5:"Sinus bradycardy",
6:"Ventricular Premature Contraction (PVC)",
7:"Supraventricular Premature Contraction",
8:"Left bundle branch block",
9:"Right bundle branch block",
10:"1. degree AtrioVentricular block",
11:"2. degree AV block",
12:"3. degree AV block",
13:"Left ventricule hypertrophy",
14:"Atrial Fibrillation or Flutter",
15:"Others",
}

$(document).ready(function (){

$('#go').on('click', function(){console.log('a')})

$('#go').on('click', function(){
    $.getJSON("/_model_data", {name:$('#name').val()}, function(data){
        model_data = data.out;
        //TODO Add graph plotting stuff
        $("#graphs").empty();
        $("#graphs").append( '<svg  height="500" class="chart"></svg>');
        var width = $('#graphs').width(),
        barHeight = 20;


    var x = d3.scaleLinear()
        .domain([0, d3.max(model_data)])
        .range([0, width]);
    
    var chart = d3.select(".chart")
        .attr("width", width)
        .attr("height", barHeight * model_data.length);
    
    var tooltip = d3.select("body").append("div").attr("class", "toolTip");

    var bar = chart.selectAll("g")
        .data(model_data)
        .enter().append("g")
        .on("mousemove", function(d,i){
            tooltip
              .style("left", d3.event.pageX + 5 + "px")
              .style("top", d3.event.pageY + 5 + "px")
              .style("display", "inline-block")
              .html(descs[i]+' , probability: '+d);
        })
    	.on("mouseout", function(d){ tooltip.style("display", "none")})
        .attr("transform", function(d, i) { return "translate(40," + i * barHeight + ")"; });
    
    bar.append("rect")
        .attr("width", x)
        .attr("height", barHeight - 1);
        console.log(x)
    bar.append("text")
        .attr("x", function(d) { console.log(d);if(d!==0){return x(d) - 3;}else {return 20} })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function(d,i) { return d; });
    
    bar.append("text")
        .attr("x", function(d) { return -10; })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function(d,i) { return "Class " + i; });
        
    
    }
);
  

    $.getJSON("/_chat_data", {name:$('#name').val()}, function(data){
        chat_data = data.out;
        $("#questions").empty();
        var html = '<h2>Problems</h2><table class="table"><thead><th>Problem</th><th>Severity</th><th>Time</th></thead><tbody>';
        for (var i=0; i<chat_data.length; i++){
            html+='<tr>'
            for (var key in chat_data[i]){
                html+='<td>'+chat_data[i][key]+'</td>'
            }
            html+='</tr>'
        }
        html+='</tbody></table>'
        $('#questions').append(html)

        $("#cal").empty();

        var pains = [];
        var times = [];
        var p=[];
        for (var i=0; i<chat_data.length; i++){
            pains.push(chat_data[i]["pain"])
            times.push(chat_data[i]["time"])
            p.push({[chat_data[i]["pain"]] : chat_data[i]["time"]})
        }

        $("#cal").append( '<svg width="960" height="500" id="chart1"></svg>');
        var width = $('#cal').width(),
        barHeight = 20;
        var x = d3.scaleLinear()
            .domain([0, d3.max(times)])
            .range([0, width]);
            
        var chart = d3.select("#chart1")
            .attr("width", width)
            .attr("height", barHeight * chat_data.length);

            console.log(d3.max(pains.map((x=>x.length))));
        
        var tooltip = d3.select("body").append("div").attr("class", "toolTip");
            
        var l = d3.max(pains.map((x=>x.length)))*10

        var bar = chart.selectAll("g")
            .data(chat_data)
            .enter().append("g")
            .on("mousemove", function(d,i){
                tooltip
                  .style("left", d3.event.pageX + 5 + "px")
                  .style("top", d3.event.pageY + 5 + "px")
                  .style("display", "inline-block")
                  .html(d.pain+' issue , severity: '+d.scale+' for '+d.time+' days.');
            })
            .on("mouseout", function(d){ tooltip.style("display", "none")})    
            .attr("transform", function(d, i) { return "translate("+l +"," + i * barHeight + ")"; });
        
            console.log(x)

        bar.append("rect")
            .attr("width", function(d){return x(d.time)})
            .attr("height", barHeight - 1)
            .style("fill", function(d){var a=d.scale*10;return "hsl(+"+a+", 100%, 50%)"});

        bar.append("text")
            .attr("x", function(d) {return -l; })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return d.pain; });
    
        });
    });
})

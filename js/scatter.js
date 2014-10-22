
var makeFigure = function(){

  var margin = {top: 30, right: 100, bottom: 30, left: 100},
      width = $("#canvas-svg").width() - margin.left - margin.right,
      height =  $("#canvas-svg").width()*0.4 - margin.top - margin.bottom;

  /*var x = d3.scale.linear().range([0, width]);*/

  /*var y = d3.scale.linear().range([height, 0]);*/
  var x = d3.scale.log().range([0,width]);
  var y = d3.scale.log().range([height, 0]);

  var color = d3.scale.category20();

  var xAxis = d3.svg.axis().scale(x).orient("bottom");

  var yAxis = d3.svg.axis().scale(y).orient("left");

  var svg = d3.select("#canvas-svg").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.csv("./data/pay_and_rec.csv", function(error, data) {
    data.forEach(function(d) {
      if (d.p<=0) {d.p = 1e6}
      if (d.r<=0) {d.r = 1e6}
      d.pay = d.p/1e6; // 數字
      d.rec = d.r/1e6;   // 數字
    });

    x.domain(d3.extent(data, function(d) { return d.pay; })).nice();
    y.domain(d3.extent(data, function(d) { return d.rec; })).nice();

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
      .append("text")
        .attr("class", "label")
        .attr("x", width)
        .attr("y", -6)
        .style("text-anchor", "end")
        .text("支出(百萬新台幣)");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("class", "label")
        /*.attr("transform", "rotate(-90)")*/
        .attr("transform", "translate(200,0)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("收入(百萬新台幣)")

    svg.selectAll(".dot")
        .data(data)
      .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 10)
        .attr("cx", function(d) { return x(d.pay); })
        .attr("cy", function(d) { return y(d.rec); })
        .style("fill", function(d) { return color("第"+d.term+"屆"+d.position1+"-"+d.account1); })
        .on("mouseover", function(d) {
            d3.select(this)
            .transition()
            .attr("r",30);

            svg.selectAll(".tipsg")
            .data([d])
            .enter().append("rect")
            .attr("class","tipsg")
            .text("第"+d.term+"屆"+d.position1)
            .attr("x", function(d) {return ((x(d.pay)-150)<0)?x(d.pay)+40:x(d.pay)-160;})
            .attr("y", function(d) {return y(d.rec)-40;})
            .attr("width",130)
            .attr("height",140)
            ;




            svg.selectAll(".tips")
            .data([d])
            .enter().append("text")
            .attr("class","tips")
            .text("第"+d.term+"屆"+d.position1)
            .attr("x", function(d) {return ((x(d.pay)-150)<0)?x(d.pay)+50:x(d.pay)-150;})
            .attr("y", function(d) {return y(d.rec);})
            ;

             svg.selectAll(".tips2")
            .data([d])
            .enter().append("text")
            .attr("class","tips2")
            .text(d.account1)
            .attr("x", function(d) {return ((x(d.pay)-150)<0)?x(d.pay)+50:x(d.pay)-150;})
            .attr("y", function(d) {return y(d.rec)-20;});


            svg.selectAll(".tips3")
            .data([d])
            .enter().append("text")
            .attr("class","tips3")
            .text(function(d){ return (d.pay!=1)? "支出:"+Math.floor(d.pay)+"百萬元": "n/a"})
            .attr("x", function(d) {return ((x(d.pay)-150)<0)?x(d.pay)+50:x(d.pay)-150;})
            .attr("y", function(d) {return y(d.rec)+20;});
            svg.selectAll(".tips4")
            .data([d])
            .enter().append("text")
            .attr("class","tips4")
            .text(function(d){ return (d.rec!=1)? "收入:"+Math.floor(d.rec)+"百萬元":"n/a"})
            .attr("x", function(d) {return ((x(d.pay)-150)<0)?x(d.pay)+50:x(d.pay)-150;})
            .attr("y", function(d) {return y(d.rec)+40;});



             })
        .on("mouseout", function() {
            d3.select(this)
            .transition()
            .attr("r",10);
            d3.selectAll(".tips").remove();
            d3.selectAll(".tips2").remove();
            d3.selectAll(".tips3").remove();
            d3.selectAll(".tips4").remove();
            d3.selectAll(".tipsg").remove();
            });



        ;

    var legend = svg.selectAll(".legend")
        .data(color.domain())
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .attr("id",function(d){return "candidate"+d.No})
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });
    var line = d3.svg.line()
    .x(function(d) { return x(d[0]); })
    .y(function(d) { return y(d[1]); });

    svg.append("path")
    .datum(d3.range(10).map(function(x) { return [x*5e1+1, x*5e1+1]; }))
    .attr("class", "line")
    .attr("d", line);
    svg.append("path")
    .datum(d3.range(10).map(function(x) { return [x*5e1+1, 2*x*5e1+1]; }))
    .attr("class", "doubleline")
    .attr("d", line);
    svg.append("path")
    .datum(d3.range(5).map(function(x) { return [2*x*5e1+1, x*5e1+1]; }))
    .attr("class", "doubleline")
    .attr("d", line);



  });
};

$(function(){


  makeFigure();
  
  
  // Begin of Settings
  $(".navbar-header .navbar-brand").attr("href",NAVBAR_BRNAD_LINK).html(NAVBAR_BRAND);
  $(".navbar-nav a:contains('圖表資料來源')").attr("href",FIGURES_DATA_SRC_LINK);
  $(".dropdown-menu a:contains('提供者')").attr("href",RAW_DATA_PROVIDER_LINK).html("提供者-"+RAW_DATA_PROVIDER_NAME);
  $(".dropdown-menu a:contains('資料產生網站')").attr("href",RAW_DATA_PROVIDER_WEBSITE_LINK).html("資料產生網站-"+RAW_DATA_PROVIDER_WEBSITE_NAME);
  $(".dropdown-menu a:contains('資料整理')").attr("href",DATA_ETL_WEBSITE_LINK).html("資料整理-"+DATA_ETL_WEBSITE_NAME);
  $(".navbar-nav a:contains('@aha')").attr("href",CONTACT_ME);
  // End of Settings






});

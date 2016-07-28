function tooltipBarChart(chartdata, namedata) {
  /* Create a bar chart with tooltips on hover.
  Input arrays need to be of same length.

  Input: Array[int] chartdata,
          Array[str] namedata
  */

  //  the size of the overall svg element
  var maxValue = Math.max.apply(Math, chartdata);
  var height = maxValue;
  var width = 1000;
   
  //  the width of each bar and the offset between each bar
  var barOffset = 1;
  var barWidth = (width/namedata.length) - barOffset;

  var tooltip = d3.select('body').append('div')
  		.style('position','absolute') //To allow d3 to follow the position absolute to the relationship to the page
  		.style('padding','0 10px') //To do padding on the toop tip. 0 on the top and bottom and 10px on each side
  		.style('background','white')
  		.style('color', '#888')
  		.style('opacity',0)

  var graph = d3.select('#chart').append('svg')
    .attr('width', width)
    .attr('height', height)
    .selectAll('rect').data(chartdata)
    .enter().append('rect')
      .style({'fill': '#FBE4DC', 'stroke': '#FBE4DC', 'stroke-width': '1'})
      .attr('width', barWidth)
      .attr('height', function (data) {
          return data;
      })
      .attr('x', function (d, i) {
          return i*barWidth;
      })
      .attr('y', function (d) {
          return (height - d)/2;
      })
      .on('mouseover', function(data, i) {
          tooltip.transition().style('opacity',.9); // show tooltip
        	tooltip.html(namedata[i] + ' (' + chartdata[i] + ')')
        		.style('left',(d3.event.pageX - 10)+ 'px') //position of the tooltip
        		.style('top',(d3.event.pageY - 40) + 'px');
          dynamicColor = this.style.fill;
          d3.select(this)
              .style('stroke', '#c34528')
              .style('fill', '#c34528');
      })
      .on('mouseout', function(data) {
      	tooltip.transition()
        	.style('opacity', 0); // hide tooltip
          d3.select(this)
              .style('stroke', '#FBE4DC')
              .style('fill', '#FBE4DC');
      });
}


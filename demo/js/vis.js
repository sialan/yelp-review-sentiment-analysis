var Bubbles = function() {
  var chart, clear, click, collide, collisionPadding, connectEvents, data, force, gradient, gradientValue, gravity, hashchange, height, idValue, jitter, label, margin, maxRadius, minCollisionRadius, mouseout, mouseover, node, rScale, rValue, textValue, tick, transformData, update, updateActive, updateLabels, updateNodes, width;
  width = window.innerWidth;
  height = window.innerWidth * 510 / 980 * 13 / 20;
  data = [];
  node = null;
  label = null;
  margin = {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  };
  maxRadius = 65;
  rScale = d3.scale.sqrt().range([0, maxRadius]);
  rValue = function(d) {
    return parseInt(d.count);
  };
  idValue = function(d) {
    return d.name.replace(/ /g,"-");
  };
  nSentimentValue = function(d) {
    return parseInt(d.negative);
  };
  pSentimentValue = function(d) {
    return parseInt(d.positive);
  };
  reviewIds = function(d) {
    return d.review_ids;
  }
  gradientId = function(d) {
    return idValue(d) + "-sentiment";
  };
  createGradientValue = function(d) {
    var svg = d3.select('svg#vis-main');
    // Define the gradient
    gradient = svg.append("svg:defs")
        .attr("id", gradientId(d))
        .append("svg:linearGradient")
        .attr("id", gradientId(d) + "-gradient")
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "0%")
        .attr("spreadMethod", "pad");

    // Define the gradient colors
    gradient.append("svg:stop")
        .attr("offset", pSentimentValue(d).toString() + "%")
        .attr("stop-color", "#d9f4d5")
        .attr("stop-opacity", 1);
    gradient.append("svg:stop")
        .attr("offset", pSentimentValue(d).toString() + "%")
        .attr("stop-color", "#ffa19c")
        .attr("stop-opacity", 1);
    return 'url(#' + gradientId(d) + '-gradient)';
  };
  resetGradientValue = function(d) {
    var svg = d3.select('svg#vis-main');
    var oldGradDef = d3.select('#' + gradientId(d)).remove();

    // Define the gradient
    gradient = svg.append("svg:defs")
        .attr("id", gradientId(d))
        .append("svg:linearGradient")
        .attr("id", gradientId(d) + "-gradient")
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "0%")
        .attr("spreadMethod", "pad");

    // Define the gradient colors
    gradient.append("svg:stop")
        .attr("offset", pSentimentValue(d).toString() + "%")
        .attr("stop-color", "#d9f4d5")
        .attr("stop-opacity", 1);
    gradient.append("svg:stop")
        .attr("offset", pSentimentValue(d).toString() + "%")
        .attr("stop-color", "#ffa19c")
        .attr("stop-opacity", 1);
    return 'url(#' + gradientId(d) + '-gradient)';
  };
  updateActiveGradient = function(d) {
    var svg = d3.select('svg#vis-main');
    var oldGradDef = d3.select('#' + gradientId(d)).remove();

    // Define the gradient
    gradient = svg.append("svg:defs")
        .attr("id", gradientId(d))
        .append("svg:linearGradient")
        .attr("id", gradientId(d) + "-gradient")
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "0%")
        .attr("spreadMethod", "pad");

    // Define the gradient colors
    gradient.append("svg:stop")
        .attr("offset", pSentimentValue(d).toString() + "%")
        .attr("stop-color", "#69ff69")
        .attr("stop-opacity", 1);
    gradient.append("svg:stop")
        .attr("offset", pSentimentValue(d).toString() + "%")
        .attr("stop-color", "#ff697e")
        .attr("stop-opacity", 1);
    return 'url(#' + gradientId(d) + '-gradient)';
  };
  xStartValue = function(d) {
    return d.positive;
  };
  textValue = function(d) {
    return d.name;
  };
  collisionPadding = 4;
  minCollisionRadius = 12;
  jitter = 0.2;
  transformData = function(rawData) {
    rawData.forEach(function(d) {
      d.count = parseInt(d.count);
      d.positive = parseInt(d.positive);
      d.negative = parseInt(d.negative);
      return rawData.sort(function() {
        return 0.5 - Math.random();
      });
    });
    return rawData;
  };
  tick = function(e) {
    var dampenedAlpha;
    dampenedAlpha = e.alpha * 0.15;
    // node.attr("cx", function(d) { return d.x = Math.max(rValue(d) / 4, Math.min(width, d.x)); }) .attr("cy", function(d) { return d.y = Math.max(rValue(d), Math.min(height - rValue(d), d.y)); });
    node.each(gravity(dampenedAlpha)).each(collide(jitter)).attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
    return label.style("left", function(d) {
      return ((margin.left + d.x) - d.dx / 2) + "px";
    }).style("top", function(d) {
      return ((margin.top + d.y) - d.dy / 2) + "px";
    });
  };
  force = d3.layout.force()
    .gravity(0)
    .charge(0)
    .size([width, height])
    .on("tick", tick);
  chart = function(selection) {
    return selection.each(function(rawData) {
      var maxDomainValue, svg, svgEnter;
      data = transformData(rawData);
      maxDomainValue = d3.max(data, function(d) {
        return rValue(d);
      });
      rScale.domain([0, maxDomainValue]);
      svg = d3.select(this).selectAll("svg").data([data]);
      svgEnter = svg.enter().append("svg");
      svg.attr("width", width + margin.left + margin.right);
      svg.attr("height", height + margin.top + margin.bottom);
      svg.attr("id", "vis-main");
      // svg.append("svg:defs").attr("id", "sentiment-gradients");
      node = svgEnter.append("g").attr("id", "bubble-nodes").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      node.append("rect").attr("id", "bubble-background").attr("width", width).attr("height", height).on("click", clear);
      label = d3.select(this).selectAll("#bubble-labels").data([data]).enter().append("div").attr("id", "bubble-labels");
      update();
      hashchange();
      return d3.select(window).on("hashchange", hashchange);
    });
  };
  update = function() {
    data.forEach(function(d, i) {
      return d.forceR = Math.max(minCollisionRadius, rScale(rValue(d)));
    });
    force.nodes(data).start();
    updateNodes();
    return updateLabels();
  };
  updateNodes = function() {
    node = node.selectAll(".bubble-node").data(data, function(d) {
      return idValue(d);
    });
    node.exit().remove();
    return node.enter().append("a").attr("class", "bubble-node").attr("xlink:href", function(d) {
      return "#" + (encodeURIComponent(idValue(d)));
    }).call(force.drag).call(connectEvents).append("circle").attr("r", function(d) {
      return rScale(rValue(d));
    })
    // Fill the circle with the gradient
    .attr('fill', function(d) {
      return createGradientValue(d);
    });
  };
  updateLabels = function() {
    var labelEnter;
    label = label.selectAll(".bubble-label").data(data, function(d) {
      return idValue(d);
    });
    label.exit().remove();
    labelEnter = label.enter().append("a").attr("class", "bubble-label").attr("href", function(d) {
      return "#" + (encodeURIComponent(idValue(d)));
    }).call(force.drag).call(connectEvents);
    labelEnter.append("div").attr("class", "bubble-label-name").text(function(d) {
      return textValue(d);
    });
    labelEnter.append("div").attr("class", "bubble-label-value").text(function(d) {
      return rValue(d);
    });
    label.style("font-size", function(d) {
      return Math.max(8, rScale(rValue(d) / 3.5)) + "px";
    }).style("width", function(d) {
      return 2.5 * rScale(rValue(d)) + "px";
    });
    label.append("span").text(function(d) {
      return textValue(d);
    }).each(function(d) {
      return d.dx = Math.max(2.5 * rScale(rValue(d)), this.getBoundingClientRect().width);
    }).remove();
    label.style("width", function(d) {
      return d.dx + "px";
    });
    return label.each(function(d) {
      return d.dy = this.getBoundingClientRect().height;
    });
  };
  gravity = function(alpha) {
    var ax, ay, cx, cy;
    cx = width / 2;
    cy = height / 2;
    ax = alpha / 8;
    ay = alpha;
    return function(d) {
      d.x += (cx - d.x) * ax;
      return d.y += (cy - d.y) * ay;
    };
  };
  collide = function(jitter) {
    return function(d) {
      return data.forEach(function(d2) {
        var distance, minDistance, moveX, moveY, x, y;
        if (d !== d2) {
          x = d.x - d2.x;
          y = d.y - d2.y;
          distance = Math.sqrt(x * x + y * y);
          minDistance = d.forceR + d2.forceR + collisionPadding;
          if (distance < minDistance) {
            distance = (distance - minDistance) / distance * jitter;
            moveX = x * distance;
            moveY = y * distance;
            d.x -= moveX;
            d.y -= moveY;
            d2.x += moveX;
            return d2.y += moveY;
          }
        }
      });
    };
  };
  connectEvents = function(d) {
    d.on("click", click);
    d.on("mouseover", mouseover);
    return d.on("mouseout", mouseout);
  };
  clear = function() {
    return location.replace("#");
  };
  click = function(d) {
    location.replace("#" + encodeURIComponent(idValue(d)));
    return d3.event.preventDefault();
  };
  hashchange = function() {
    var id;
    id = decodeURIComponent(location.hash.substring(1)).trim();
    return updateActive(id);
  };
  showReviews = function(currentNode, id) {
    //get the review_id, business_id??? and word selected
    //get review_id
    var reviewList = reviewIds(currentNode)
    var json
    var items = []
    $.getJSON("../data/data.json", function(data) {
      $.each(data, function(key, val) {
        $.each(val, function(ke, va) {
          if(ke === id) {
            $.each(va, function(k, v) {
              $.each(v, function(x, y) {
                if(reviewList.indexOf(x) >= 0) {
                  var temp = y['snippet'].indexOf(id);
                  var str = '';
                  if(y['polarity'] > 0) {
                    str = y['snippet'].slice(0, temp) + "<span style='background:#69ff69'>" + y['snippet'].slice(temp, temp + id.length) + "</span>" + y['snippet'].slice(temp + id.length);
                  } else if (y['polarity'] <= 0) {
                    str = y['snippet'].slice(0, temp) + "<span style='background:#ff697e'>" + y['snippet'].slice(temp, temp + id.length) + "</span>" + y['snippet'].slice(temp + id.length);
                  } else {
                    str = y['snippet'];
                  }

                  console.log(str);
                  items.push( "<dt> <strong>Polarity: " + Math.round(y['polarity']*100) /100 + "</strong></dt>" + "<dd id='review-text'>" + str + "</dd><br>" );
                }
              });

            });
          }
        });

      });
      $('.review-list').remove()
      $( "<ul>", {
        "class": "review-list",
        html: items.join( "" )
      }).appendTo( "#review" );
    });
  };
  updateActive = function(id) {
    // Set the new active gradient
    var currentNode;
    d3.selectAll(".bubble-node").attr('fill', function(d) {
      if (idValue(d) == id) {
        currentNode = d;
        return updateActiveGradient(d);
      } else {
        return resetGradientValue(d);
      };
    });
    node.classed("bubble-selected", function(d) {
      return id === idValue(d);
    });
    if (id.length > 0) {
      showReviews(currentNode, id)
      d3.select("#status").html("<h3>" + rValue(currentNode) + " reviews about <span class=\"active\">" + id + "</span> for <a target='_blank' href='http://www.yelp.com/biz/bristled-boar-saloon-and-grill-middleton'>Bristled Boar Saloon & Grill</a> shown below (<span class='positive-sentiment'>" + pSentimentValue(currentNode) + "% positive</span>, <span class='negative-sentiment'>" + nSentimentValue(currentNode) + "% negative</span>):</h3>");
    } else {
      d3.select("#status").html("<h3>No word is active</h3>");
    }
  };
  mouseover = function(d) {
    return node.classed("bubble-hover", function(p) {
      return p === d;
    });
  };
  mouseout = function(d) {
    return node.classed("bubble-hover", false);
  };
  chart.jitter = function(_) {
    if (!arguments.length) {
      return jitter;
    }
    jitter = _;
    force.start();
    return chart;
  };
  chart.height = function(_) {
    if (!arguments.length) {
      return height;
    }
    height = _;
    return chart;
  };
  chart.width = function(_) {
    if (!arguments.length) {
      return width;
    }
    width = _;
    return chart;
  };
  chart.r = function(_) {
    if (!arguments.length) {
      return rValue;
    }
    rValue = _;
    return chart;
  };
  return chart;
};

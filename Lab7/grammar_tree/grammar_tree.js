// The actual tree data is in sample...js
//--------------------------------------------------------

var m = [20, 120, 20, 120],
    w = 1280 - m[1] - m[3],
    h = 600 - m[0] - m[2],
    i = 0,
    root;

var isDerivation = false;

var tree = d3.layout.tree()
    .size([h, w]);

var diagonal = d3.svg.diagonal()
    .projection(function (d) { return [d.y, d.x]; });

var vis = d3.select("#body").append("svg:svg")
    .attr("width", w + m[1] + m[3])
    .attr("height", h + m[0] + m[2])
    .append("svg:g")
    .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

root.x0 = h / 2;
root.y0 = 0;
update(root);

function update(source) {
    var duration = d3.event && d3.event.altKey ? 5000 : 500;

    // Compute the new tree layout.
    var nodes = tree.nodes(root)//.reverse();

    // Normalize for fixed-depth.
    nodes.forEach(function (d) { d.y = d.depth * 180; });

    // Update the nodes…
    var node = vis.selectAll("g.node")
        .data(nodes, function (d) { return d.id || (d.id = ++i); });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("svg:g")
        .attr("class", "node")
        .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", function (d) {
            //toggle(d)
            //update(d)
            if (toggle(d)) {
                update(d)
            }
            else {
                update(d.parent)
            }
        });

    nodeEnter.append("svg:circle")
        .attr("r", 1e-6)
        .style("fill", function (d) {
            if (d.isDerivation)
                return "orange"
            else if (d.isTerminal)
                return "lightsteelblue"
            else
                return "#fff";
        });

    nodeEnter.append("svg:text")
        .attr("x", function (d) { return d.isTerminal || d.isDerivation ? 10 : -10; })
        .attr("dy", ".35em")
        .attr("text-anchor", function (d) { return d.isTerminal || d.isDerivation ? "start" : "end"; })
        .text(function (d) { return d.name; })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; });

    nodeUpdate.select("circle")
        .attr("r", 4.5)
        .style("fill", function (d) {
            if (d.isDerivation)
                return "orange"
            else if (d.isTerminal)
                return "lightsteelblue"
            else
                return "#fff";
        });

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = vis.selectAll("path.link")
        .data(tree.links(nodes), function (d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("svg:path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
            var o = { x: source.x0, y: source.y0 };
            return diagonal({ source: o, target: o });
        })
        .transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
            var o = { x: source.x, y: source.y };
            return diagonal({ source: o, target: o });
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

function jsonCopy(src) {
    return JSON.parse(JSON.stringify(src));
}

// Toggle children.
function toggle(d) {
    if (!d.isDerivation) {
        if (d.children) {
            d.children = null;
        } else {
            d.children = jsonCopy(derivations[d.name])
            d.children.forEach(function (c) { c.isDerivation = true; })
        }
        return true;
    }
    else if (!d.isTerminal) {
        d.parent.children = jsonCopy(derived_children[d.name])
        return false;
    }
}

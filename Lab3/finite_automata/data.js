
var nodes = new vis.DataSet(nodes_json);
var edges = new vis.DataSet(edges_json);

// create a network
var container = document.getElementById('mynetwork');
var data = {
    nodes: nodes,
    edges: edges
};
var options = {};
var network = new vis.Network(container, data, options);
nodes_json = [
{ id: 0, label: 's0', color: '#7BE141' },
{ id: 1, label: 's1', color: '#ff5530' },
{ id: 2, label: 's2', color: '#98caf9' },
{ id: 3, label: 's3', color: '#98caf9' }
]
edges_json = [
{ from: 3, to: 0, arrows: 'to', color: { color: '#008fe6' }, label: 'e', font: { align: 'middle' }  },
{ from: 2, to: 3, arrows: 'to', color: { color: '#008fe6' }, label: 'i', font: { align: 'middle' }  },
{ from: 1, to: 2, arrows: 'to', color: { color: '#008fe6' }, label: 'f', font: { align: 'middle' }  },
{ from: 2, to: 3, arrows: 'to', color: { color: '#008fe6' }, label: 'e', font: { align: 'middle' }  }
]

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
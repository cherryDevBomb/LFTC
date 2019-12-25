nodes_json = [
{ id: 0, label: 's0', color: '#ff5530' },
{ id: 1, label: 's1', color: '#98caf9' },
{ id: 2, label: 's2', color: '#7BE141' },
{ id: 3, label: 's3', color: '#7BE141' }
]
edges_json = [
{ from: 0, to: 1, arrows: 'to', color: { color: '#008fe6' }, label: 'a', font: { align: 'middle' }  },
{ from: 1, to: 2, arrows: 'to', color: { color: '#008fe6' }, label: 'b', font: { align: 'middle' }  },
{ from: 1, to: 3, arrows: 'to', color: { color: '#008fe6' }, label: 'c', font: { align: 'middle' }  },
{ from: 2, to: 2, arrows: 'to', color: { color: '#008fe6' }, label: 'c', font: { align: 'middle' }  },
{ from: 3, to: 2, arrows: 'to', color: { color: '#008fe6' }, label: 'b', font: { align: 'middle' }  },
{ from: 3, to: 3, arrows: 'to', color: { color: '#008fe6' }, label: 'a', font: { align: 'middle' }  }
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
from Lab2.ea import *


def closure(ea, z):
    closure_nodes = z
    for node in z:
        queue = [node]
        while len(queue) > 0:
            current_node = queue.pop()
            for edge in ea.edges:
                if int(edge.start_node) == current_node.id:
                    if edge.label == "epsilon":
                        queue.append(ea.get_node_by_id(edge.end_node))
                        closure_nodes.append(ea.get_node_by_id(edge.end_node))
    return list(set(closure_nodes))


def delta(ea, z, c):
    delta_result = []

    for node in z:
        current_node = node
        for edge in ea.edges:
            if int(edge.start_node) == current_node.id:
                if edge.label == c:
                    delta_result.append(ea.get_node_by_id(edge.end_node))
    return list(set(delta_result))


def nea_to_dea(nea):
    dea = EA()
    dea.edge_labels = nea.edge_labels
    i = 0
    dea_node_map = {}

    q0 = closure(nea, [nea.get_start_node()])
    q_list = [q0]
    worklist = [q0]

    is_start_flag = True

    while len(worklist) > 0:
        q = worklist.pop()
        for c in nea.edge_labels:
            t = closure(nea, delta(nea, q, c))
            if len(t) > 0:
                # check if we already have the nodes
                if str(q) not in dea_node_map:
                    dea_node_map[str(q)] = i
                    i += 1
                if str(t) not in dea_node_map:
                    dea_node_map[str(t)] = i
                    i += 1

                start_node = Node(dea_node_map[str(q)])
                # check if start node
                if is_start_flag:
                    start_node.is_start = True
                    is_start_flag = False

                end_node = Node(dea_node_map[str(t)])
                # check if end node
                for node in nea.nodes:
                    if node in t and node.is_end:
                        end_node.is_end = True

                # add nodes to dea nodes set
                if start_node not in dea.nodes:
                    dea.nodes.append(start_node)
                if end_node not in dea.nodes:
                    dea.nodes.append(end_node)

                # create edge
                new_edge = Edge(str(start_node.id), str(end_node.id), c)
                dea.edges.append(new_edge)

                if t not in q_list:
                    q_list.append(t)
                    worklist.append(t)
    return dea


if __name__ == "__main__":
    nea = EA()
    nea.read_ea("input4.txt")

    dea = nea_to_dea(nea)

    # export as json
    print(dea.export_nodes_as_json())
    print()
    print(dea.export_edges_as_json())
    print()
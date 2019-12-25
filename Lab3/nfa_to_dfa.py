from Lab2.fa import *


def closure(fa, z):
    closure_nodes = z
    for node in z:
        queue = [node]
        while len(queue) > 0:
            current_node = queue.pop()
            for edge in fa.edges:
                if int(edge.start_node) == current_node.id:
                    if edge.label == "epsilon":
                        queue.append(fa.get_node_by_id(edge.end_node))
                        closure_nodes.append(fa.get_node_by_id(edge.end_node))
    return list(set(closure_nodes))


def delta(fa, z, c):
    delta_result = []

    for node in z:
        current_node = node
        for edge in fa.edges:
            if int(edge.start_node) == current_node.id:
                if edge.label == c:
                    delta_result.append(fa.get_node_by_id(edge.end_node))
    return list(set(delta_result))


def nfa_to_dfa(nfa):
    dfa = FA()
    dfa.edge_labels = nfa.edge_labels
    i = 0
    dfa_node_map = {}

    q0 = closure(nfa, [nfa.get_start_node()])
    q_list = [q0]
    worklist = [q0]

    is_start_flag = True

    while len(worklist) > 0:
        q = worklist.pop()
        for c in nfa.edge_labels:
            t = closure(nfa, delta(nfa, q, c))
            if len(t) > 0:
                # check if we already have the nodes
                if str(q) not in dfa_node_map:
                    dfa_node_map[str(q)] = i
                    i += 1
                if str(t) not in dfa_node_map:
                    dfa_node_map[str(t)] = i
                    i += 1

                start_node = Node(dfa_node_map[str(q)])
                # check if start node
                if is_start_flag:
                    start_node.is_start = True
                    is_start_flag = False

                end_node = Node(dfa_node_map[str(t)])
                # check if end node
                for node in nfa.nodes:
                    if node in t and node.is_end:
                        end_node.is_end = True

                # add nodes to dfa nodes set
                if start_node not in dfa.nodes:
                    dfa.nodes.append(start_node)
                if end_node not in dfa.nodes:
                    dfa.nodes.append(end_node)

                # create edge
                new_edge = Edge(str(start_node.id), str(end_node.id), c)
                dfa.edges.append(new_edge)

                if t not in q_list:
                    q_list.append(t)
                    worklist.append(t)
    return dfa


if __name__ == "__main__":
    nfa = FA()
    nfa.read_fa("input4.txt")
    dfa = nfa_to_dfa(nfa)
    dfa.export_as_json()
from Lab3.nfa_to_dfa import *


def hopcroft(dfa):
    print('{:50}'.format("Current partition"), end=' | ')
    print('{:20}'.format("Set"), end=' | ')
    print('{:4}'.format("Char"), end=' | ')
    print('{:40}'.format("Action"))

    dfa_end_nodes = dfa.get_end_nodes()
    other_nodes = list(set(dfa.nodes) - (set(dfa_end_nodes)))
    partitions = [dfa_end_nodes, other_nodes]
    end_partitions = []

    while partitions != end_partitions:

        end_partitions = partitions
        partitions = []
        for p_set in end_partitions:
            split_result = split(dfa, partitions, end_partitions, p_set)
            partitions = partitions + split_result

    return end_partitions


def split(dfa, partitions, end_partitions, s):
    target_map = {}
    for c in dfa.edge_labels:
        print('{:50}'.format(str(end_partitions)), end=' | ')
        print('{:20}'.format(str(s)), end=' | ')
        print('{:4}'.format(c), end=' | ')

        target_map = {}
        for node in s:
            target_partition = []
            for edge in dfa.edges:
                if int(edge.start_node) == node.id and edge.label == c:
                    target_partition = get_target_partition(partitions, int(edge.end_node))
            if str(target_partition) not in target_map.keys():
                target_map[str(target_partition)] = []
            target_map[str(target_partition)].append(node)
        # return when split found
        if len(target_map) > 1:
            print('{:40}'.format('split into' + str(list(target_map.values()))))
            break
        else:
            print('{:40}'.format('none'))

    return list(target_map.values())


def get_target_partition(partitions, node_id):
    for p in partitions:
        for elem in p:
            if elem.id == node_id:
                return p


def build_min_dfa(initial_dfa, partitions):
    new_edges = []
    new_nodes_map = {}
    i = 0
    for part in partitions:
        # create new node and save to map that stores {partition, new_node}
        part_node = Node(i)
        new_nodes_map[str(part)] = part_node

        for node in part:
            if node.is_start:
                part_node.is_start = True
            if node.is_end:
                part_node.is_end = True

            for edge in initial_dfa.edges:
                if int(edge.start_node) == node.id:
                    target_part = get_target_partition(partitions, int(edge.end_node))
                    new_edge = Edge(str(part_node.id), str(target_part), edge.label)
                    new_edges.append(new_edge)
        i += 1

    for e in new_edges:
        end_part = e.end_node
        e.end_node = str(new_nodes_map[end_part].id)

    final_min_dfa = FA()
    final_min_dfa.nodes = list(new_nodes_map.values())
    final_min_dfa.edges = list(set(new_edges))
    final_min_dfa.edge_labels = initial_dfa.edge_labels
    return final_min_dfa


if __name__ == "__main__":
    dfa = FA()
    dfa.read_fa("input/input5.txt")

    partitions = hopcroft(dfa)
    min_dfa = build_min_dfa(dfa, partitions)

    min_dfa.export_as_json()

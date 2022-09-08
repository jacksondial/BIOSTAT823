"Build Kruskal's Algorithm."

# Implement Kruskal's algorithm
# given 20 sets of values as such:
# 1,2,10
# 3,4,20
# node, node, weight
# Find maximum weight spanning tree in the graph

# Kruskal's algorithm:
# 1) sort edges by descending weight
# 2) start with T all nodes of G but empty edge set
# 3) begin with highest weight edge and repeat until n-1 edges have been added to T:
# If current edge E can be added to T without creating a cycle, then add E to T
# Move to the next edge in the sorted list of edges

# Here is the set of all edges, put edges in the final tree 1 at a time by sorted descending,
# but we can't add a new edge where there will be a cycle, and once we have n-1 edges we are done

# O(nlog(n))

# import pandas as pd


# def get_max_spanning_tree(input_filepath: str):
#     """
#     Implement Kruskal's algorithm.
#     """
#     data = pd.read_csv(input_filepath, header=None)
#     data.sort_values(by=data.columns[2], ascending=False)
#     print(data)
#     print(data.loc[1])

#     indexes_to_add = []
#     df_length = len(data)
#     for row in df_length:


#     testing = data.loc[1][1]
#     print(testing)
#     return

import csv


def get_max_spanning_tree(input_filepath: str, output_filepath: str):
    """
    Implement Kruskal's Algorithm.
    """
    with open(input_filepath, "r") as read_obj:
        csv_reader = csv.reader(read_obj)
        total_edges = list(csv_reader)
    for edge in total_edges:
        edge[2] = int(edge[2])

    sorted_total_edges = sorted(
        sorted(sorted(total_edges, key=lambda x: x[1]), key=lambda x: x[0]),
        key=lambda x: x[2],
        reverse=True,
    )
    print(sorted_total_edges)

    used_points = []
    max_tree = []
    for edge in sorted_total_edges:
        if edge[1] not in used_points:
            max_tree.append(edge)
            used_points.append(edge[0])
            used_points.append(edge[1])
        else:
            pass
    print(max_tree)
    
    with open(output_filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(max_tree)


get_max_spanning_tree("hw1/test_graph1_input.csv", "hw1/max_tree.csv")

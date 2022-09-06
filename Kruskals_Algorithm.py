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

test_file = [
    [1, 2, 4],
    [1, 3, 2],
    [1, 5, 3],
    [3, 9, 2],
    [9, 2, 1],
    [2, 6, 2],
    [2, 4, 5],
    [5, 8, 3],
    [8, 7, 1],
    [8, 4, 3],
    [4, 11, 2],
    [8, 10, 2],
    [10, 11, 3],
]

new_list = sorted(test_file, key=lambda x: x[2])

print(new_list[11][2])  # should give me a 4


def krus_alg(new_list: list[list[str]]) -> list[list[str]]:
    """
    Implement Kruskal's algorithm.
    """
    for el in new_list:
        

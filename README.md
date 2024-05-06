# GraphForge
[TDL Project](https://hmnshpl.notion.site/TDL-Project-b078c76359f94caca7e38485dc3af452?pvs=4)

```
def island_encoding():    
    list_islands = connected_components(graph)
    output += “There are {len(list_islands)}.”
    for i, island in enumerate(list_islands):
        island_nodes = list(island.nodes())
        output += += f" \n This is island {i+1} of {number_of_islands}. Contains the nodes {island_nodes}."
    return output
```


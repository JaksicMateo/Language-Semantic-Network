import networkx as nx

def get_inherited_properties(G, language_name):
    # verify that language exists in network
    if language_name not in G:
        raise ValueError(f"{language_name} is not in the network")
    
    # initialize dictionary to store the properties
    properties = {}

    # check if the node is a language node and extract its attributes
    if 'type' in G.nodes[language_name] and G.nodes[language_name]['type'] == 'language':
        properties.update({k: v for k, v in G.nodes[language_name].items() if k != 'type'})
    
    # climb the hierarchy to find shared traits
    for parent in nx.ancestors(G, language_name):
        parent_attrs = G.nodes[parent]
        
        # look through each attribute in the parent category
        for k, v in parent_attrs.items():
            # inherited traits are added only if they don't overwrite the child's specific data
            if k not in ["type", "label"] and k not in properties:
                properties[k] = v
    
    return properties

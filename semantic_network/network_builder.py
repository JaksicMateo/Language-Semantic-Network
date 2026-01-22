import json
import networkx as nx
from pathlib import Path

def build_network(json_path=None):
    # initialize directed graph
    G = nx.DiGraph()

    # loading dataset
    with open("data/language_data.json", "r", encoding="utf-8") as f:
        languages = json.load(f)

    # iterating through each language to build nodes and edges
    for lang_name, attrs in languages.items():
        # get hierarchy attributes directly
        family = attrs.get("family", "")
        branch = attrs.get("branch", "")
        subgroup = attrs.get("subgroup", "")
        
        # define unique identifiers for each level of the hierarchy
        root_category = attrs.get("description", "Unclassified Entity")
        root_node_id = f"{root_category}"
        family_node_id = f"{family}" if family else None
        branch_node_id = f"{branch}" if branch else None
        subgroup_node_id = f"{subgroup}" if subgroup else None

        # create the top level category node if it doesn't exist
        if not G.has_node(root_node_id):
            G.add_node(root_node_id, type="root_category", label=root_category)

        # process the family attribute and link it to the root
        if family:
            if not G.has_node(family):
                traits = {}
                if family == "Turkic":
                    traits = {"morphological_type": "Agglutinative", "vowel_harmony": True}
                G.add_node(family, type="family", **traits)
            G.add_edge(root_node_id, family)

        # process the branch attribute and link it to the parent family attribute
        if branch:
            if not G.has_node(branch):
                traits = {}
                if branch == "Slavic":
                    traits = {"verb_aspect": True, "gender_system": True, "vowel_harmony": False}
                G.add_node(branch, type="branch", **traits)
            if family: G.add_edge(family, branch)

        # process the subgroup attribute and link it to the parent branch attribute
        if subgroup_node_id:
            if not G.has_node(subgroup_node_id):
                G.add_node(subgroup_node_id, type="subgroup", label=subgroup)
            
            if branch_node_id:
                if not G.has_edge(branch_node_id, subgroup_node_id):
                    G.add_edge(branch_node_id, subgroup_node_id)

        G.add_node(lang_name, type="language", **attrs)

        # connecting to parent node
        if subgroup_node_id:
            G.add_edge(subgroup_node_id, lang_name)
        elif branch_node_id:
            G.add_edge(branch_node_id, lang_name)
        elif family_node_id:
            G.add_edge(family_node_id, lang_name)
        else:
            G.add_edge(root_node_id, lang_name)

    return G
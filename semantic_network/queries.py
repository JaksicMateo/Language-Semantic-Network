import networkx as nx
from semantic_network.inheritance import get_inherited_properties

# init of comparison attributes
comparison_attributes = [
    "alphabet", "digraphic", "cases", "verb_aspect", "gender_system",
    "dual_number", "definite_article", "analytic",
    "palatalization", "nasal_vowels", "soft_consonants",
    "loanwords_influence", "mutual_intelligibility", "subgroup"]

# finds branches connected to the family
def query1_branches_in_family(G, family):
    if family not in G:
        return []
    
    return [
        n for n in G.successors(family)
        if G.nodes[n].get("type") == "branch"
    ]

# finds subgroups connected to the branch
def query2_subgroups_in_branch(G, branch):
    if branch not in G:
        return []

    return [
        n for n in G.successors(branch)
        if G.nodes[n].get("type") == "subgroup"
    ]

# finds languages connected to the subgroup
def query3_languages_in_subgroup(G, subgroup):
    if subgroup not in G:
        return []

    return [
        n for n in G.successors(subgroup)
        if G.nodes[n].get("type") == "language"
    ]

# finds languages connected to the alphabet
def query4_languages_by_alphabet(G, alphabet):
    results = []
    for n, d in G.nodes(data=True):
        if d.get("type") == "language":
            systems = d.get("writing_system", [])
            if isinstance(systems, list):
                if alphabet in systems:
                    results.append(n)
            elif isinstance(systems, str):
                if systems == alphabet:
                    results.append(n)
    return results

# finds languages connected to morphological type
def query5_languages_by_morphological(G, morphological):
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language" and d.get("morphological_type") == morphological
    ]

# finds languages connected to word order
def query6_languages_by_order(G, order):
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language" and d.get("word_order") == order
    ]

# finds languages connected to writing direction
def query7_languages_by_direction(G, direction):
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language" and d.get("text_direction") == direction
    ]

# finds languages connected to tone system
def query8_languages_by_tone(G, tone):
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language" and d.get("tone_system") == tone
    ]

# finds languages connected to number of cases
def query9_languages_by_cases(G, number, mode):
    result = []
    for n, d in G.nodes(data=True):
        if d.get("type") == "language":
            cases = d.get("cases")
            if (mode == "more" and cases > number) or (mode == "less" and cases < number):
                result.append(f"{n} ({int(cases)})")
            elif (mode == "equal" and cases == number):
                result.append(n)
    return result

# finds languages connected to loanwords influence
def query10_influenced_by(G, language):
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language"
        and language in d.get("loanwords_influence", [])
    ]    

# finds languages connected to mutually intelligibility
def query11_mutually_intelligible(G, language):
    result = set()
    
    if language in G:
        data = G.nodes[language]
        result.update(data.get("mutual_intelligibility", []))

    for n, d in G.nodes(data=True):
        if d.get("type") == "language" and language in d.get("mutual_intelligibility", []):
            result.add(n)

    return sorted(result)

# finds inherited properties connected to language
def query12_inherited_properties(G, language):
    return get_inherited_properties(G, language)

# finds shortest path between two languages
def query13_shortest_path(G, lang1, lang2):
    try:
        undirected = G.to_undirected()
        path = nx.shortest_path(undirected, source=lang1, target=lang2)
        return path
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None

# finds languages connected to boolean property
def query14_languages_with_property(G, property_name):
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language" and d.get(property_name) is True
    ]

# finds languages connected to combination of attributes
def query15_combined_conditions(G, attributes):
    matched = []
    langs = [n for n, d in G.nodes(data=True) if d.get("type") == "language"]
    
    for n in langs:
        props = get_inherited_properties(G, n)
        if all(props.get(attr) for attr in attributes):
            matched.append(n)

    return matched

# finds shared properties between two languages 
def query16_shared_properties(G, lang1, lang2):
    props1 = get_inherited_properties(G, lang1)
    props2 = get_inherited_properties(G, lang2)

    shared = []
    for attr in comparison_attributes:
        v1 = props1.get(attr)
        v2 = props2.get(attr)

        if v1 is None and v2 is None:
            continue

        if isinstance(v1, list) and isinstance(v2, list):
            if set(v1) == set(v2) and v1:
                shared.append(attr)
        elif v1 == v2:
            shared.append(attr)

    return shared

# finds different properties between two languages 
def query17_different_properties(G, lang1, lang2):
    props1 = get_inherited_properties(G, lang1)
    props2 = get_inherited_properties(G, lang2)

    different = []
    for attr in comparison_attributes:
        v1 = props1.get(attr)
        v2 = props2.get(attr)
        
        if v1 != v2:
            different.append(attr)

    return different

# function for calculating properties similarity between two languages
def calculate_similarity(props1, props2):
    count = 0
    for attr in comparison_attributes:
        v1 = props1.get(attr)
        v2 = props2.get(attr)
        if isinstance(v1, list) and isinstance(v2, list):
            if set(v1) == set(v2) and v1:
                count += 1
        elif v1 == v2 and v1 is not None:
            count += 1
    return count

# finds language with most similarities
def query18_most_similar_language(G, language):
    target_props = get_inherited_properties(G, language)
    max_shared = -1
    best = []

    for other, d in G.nodes(data=True):
        if other == language or d.get("type") != "language":
            continue

        other_props = get_inherited_properties(G, other)
        shared_count = calculate_similarity(target_props, other_props)
        
        if shared_count > max_shared:
            max_shared = shared_count
            best = [other]
        elif shared_count == max_shared:
            best.append(other)

    return best, max_shared

# finds language with least similarities
def query19_most_different_language(G, language):
    target_props = get_inherited_properties(G, language)
    min_shared = float("inf")
    worst = []

    for other, d in G.nodes(data=True):
        if other == language or d.get("type") != "language":
            continue

        other_props = get_inherited_properties(G, other)
        shared_count = calculate_similarity(target_props, other_props)
        
        if shared_count < min_shared:
            min_shared = shared_count
            worst = [other]
        elif shared_count == min_shared:
            worst.append(other)

    return worst, min_shared

# finds values for language properties
def query20_language_property(G, language, attribute):
    props = get_inherited_properties(G, language)
    return props.get(attribute, "Unknown")

# finds languages by language status
def query21_status(G, status_type):
    if status_type == "living natural":
        return [
            n for n, d in G.nodes(data=True)
            if d.get("type") == "language" 
            and d.get("constructed") is False 
            and d.get("extinct") is False
        ]
    
    return [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "language" and d.get(status_type) is True
    ]
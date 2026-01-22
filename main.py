import tkinter as tk
from tkinter import ttk, messagebox
from semantic_network import build_network
from semantic_network.queries import *
from semantic_network.inheritance import get_inherited_properties

# tkinter root
root = tk.Tk()
root.title("Languages Semantic Network")
root.geometry("950x600")
welcome_frame = tk.Frame(root)
welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
query_frame = tk.Frame(root)
question_label = tk.Label(query_frame, text="", wraplength=900, font=("Arial", 12, "bold"))
question_label.pack(pady=5)
input_frame = tk.Frame(query_frame)
input_frame.pack(pady=5, fill="x")
result_frame = tk.Frame(query_frame)
result_frame.pack(fill="both", expand=True, pady=10)
result_text = tk.Text(result_frame, height=12)
result_text.pack(side="left", fill="both", expand=True)
scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)

# building network
G = build_network()

# initializing lists and state variables
families = sorted([n for n, d in G.nodes(data=True) if d.get("type") == "family" and n != "Constructed"])
branches = sorted([n for n, d in G.nodes(data=True) if d.get("type") == "branch" and n != "None"])
subgroups = sorted([n for n, d in G.nodes(data=True) if d.get("type") == "subgroup" and n != "None"])
languages = sorted([n for n, d in G.nodes(data=True) if d.get("type") == "language"])
influences = sorted({src for _, d in G.nodes(data=True) if d.get("type") == "language" for src in d.get("loanwords_influence", [])})
boolean_attributes = sorted(["digraphic", "verb_aspect", "gender_system", "dual_number", "definite_article", "vowel_harmony", "palatalization", "nasal_vowels"])
attributes = sorted(["digraphic", "verb_aspect", "gender_system", "dual_number", "subgroup", "cases", "writing_system", "definite_article", "palatalization",
                "nasal_vowels", "loanwords_influence", "mutual_intelligibility", "text_direction", "tone_system", "speakers_total", "constructed", "extinct"])
alphabets = sorted(["Cyrillic", "Latin", "Greek", "Arabic", "Devanagari", "Persian", "Bengali", "Gurmukhi", "Shahmukhi", "Logographic", "Abjad", "Gothic", "Glagolitic", "Birch Bark Cursive",
             "Syllabary", "Hangul", "Thai", "Burmese", "Hebrew", "Cuneiform", "Armenian", "Mkhedruli", "Osmanya", "pIqaD", "Tengwar", "Runes", "Coptic", "Cuneiform", "Western Cyrillic",
             "Mayan Hieroglyphs", "Oracle Bone Script", "Seal Script", "Syriac"])
morphologies = sorted(["Fusional", "Analytic", "Analytic-Fusional", "Agglutinative", "Agglutinative-Inflexional",  "Introflexive", "Introflexive-Fusional",
                "Isolating", "Agglutinative-Analytic", "Agglutinative-Fusional"])
orders = sorted(["Flexible", "SVO", "V2", "SVO/V2", "SOV", "VSO/SVO", "VSO/VOS", "Topic-prominent", "SVO/SOV", "V2/SOV", "VSO", "OVS", "VOS"])
directions = sorted(["Left to right", "Right to left", "Paired columns", "Vertical"])
tones = sorted(["Non-tonal", "Pitch Accent", "Tonal"])
compares = sorted(["equal", "more", "less"])
statuses = ["constructed", "extinct", "living natural"]

family_var = tk.StringVar(value=families[0])
branch_var = tk.StringVar(value=branches[0])
subgroup_var = tk.StringVar(value=subgroups[0])
language_var = tk.StringVar(value=languages[0])
language2_var = tk.StringVar(value=languages[1])
alphabet_var = tk.StringVar(value=alphabets[0])
number_var = tk.StringVar(value="0")
property_var = tk.StringVar(value=sorted(boolean_attributes)[0])
attribute_var = tk.StringVar(value=sorted(attributes)[0])
compare_var = tk.StringVar(value=compares[0])
checkbox_vars = {attr: tk.BooleanVar() for attr in boolean_attributes}
influence_var = tk.StringVar(value=influences[0])
morphological_var = tk.StringVar(value=morphologies[0])
tone_var = tk.StringVar(value=tones[0])
order_var = tk.StringVar(value=orders[0])
direction_var = tk.StringVar(value=directions[0])
status_var = tk.StringVar(value=statuses[0])

# queries
queries = {
    "Q1": {"text": "Which branches belong to the <name> language family?", "inputs": ["single_family"]},
    "Q2": {"text": "Which subgroups belong to the <name> language branch?", "inputs": ["single_branch"]},
    "Q3": {"text": "Which languages belong to the <name> language subgroup?", "inputs": ["single_subgroup"]},
    "Q4": {"text": "Which languages use the <name> writing system?", "inputs": ["alphabet"]},
    "Q5": {"text": "Which languages have the <name> morphological type?", "inputs": ["morphological"]},
    "Q6": {"text": "Which languages have the <name> word order?", "inputs": ["order"]},
    "Q7": {"text": "Which languages have the <name> text direction?", "inputs": ["direction"]},
    "Q8": {"text": "Which languages have the <name> tone system?", "inputs": ["tone"]},
    "Q9": {"text": "Which languages have <compare> to/than <number> cases?", "inputs": ["compare", "number"]},
    "Q10": {"text": "Which languages are influenced by <language>?", "inputs": ["influence_lang"]},
    "Q11": {"text": "Which languages are mutually intelligible with <language>?", "inputs": ["single_lang"]},
    "Q12": {"text": "Which properties are inherited from a <language>?", "inputs": ["single_lang"]},
    "Q13": {"text": "What is the shortest path between <language1> and <language2> in the hierarchy?", "inputs": ["two_langs"]},
    "Q14": {"text": "Which languages have the <name> property?", "inputs": ["property"]},
    "Q15": {"text": "Which languages satisfy a combination of attributes?", "inputs": ["attributes"]},
    "Q16": {"text": "What are shared properties between <language1> and <language2>?", "inputs": ["two_langs"]},
    "Q17": {"text": "What are different properties between <language1> and <language2>?", "inputs": ["two_langs"]},
    "Q18": {"text": "Which language is most similar to <language>?", "inputs": ["single_lang"]},
    "Q19": {"text": "Which language is most different from <language>?", "inputs": ["single_lang"]},
    "Q20": {"text": "What property does <language> have for <attribute>?", "inputs": ["single_lang", "attribute"]},
    "Q21": {"text": "Which languages have the <name> status?", "inputs": ["status"]}
}
queries_order = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15","Q16","Q17","Q18","Q19","Q20","Q21"]

# helper functions for formatted output
def clear_result():
    result_text.delete(1.0, tk.END)

def display_result(text):
    clear_result()
    result_text.insert(tk.END, text)

def format_list_output(title, items):
    if not items:
        return f"{title}\nNo results found."
    lines = [f"{i+1}. {item}" for i, item in enumerate(items)]
    return f"{title}\n" + "\n".join(lines)

def format_single_output(title, value):
    return f"{title}\n{value}"

# run query
def run_query(selected_q):
    try:
        q = selected_q.split(":")[0]

        if q == "Q1":
            family = family_var.get()
            branchs = query1_branches_in_family(G, family)
            text = format_list_output(f"Branches in {family} language family are:", sorted(branchs))

        elif q == "Q2":
            branch = branch_var.get()
            subgrs = query2_subgroups_in_branch(G, branch)
            text = format_list_output(f"Subgroups in {branch} language branch are:", sorted(subgrs))

        elif q == "Q3":
            subgroup = subgroup_var.get()
            langs = query3_languages_in_subgroup(G, subgroup)
            text = format_list_output(f"Languages in {subgroup} subgroup are:", sorted(langs))

        elif q == "Q4":
            alphabet = alphabet_var.get()
            langs = query4_languages_by_alphabet(G, alphabet)
            text = format_list_output(f"Languages using {alphabet} writing system are:", sorted(langs))

        elif q == "Q5":
            morphological = morphological_var.get()
            langs = query5_languages_by_morphological(G, morphological)
            text = format_list_output(f"Languages using {morphological} morphological type are:", sorted(langs))

        elif q == "Q6":
            order = order_var.get()
            langs = query6_languages_by_order(G, order)
            text = format_list_output(f"Languages using {order} word order are:", sorted(langs))

        elif q == "Q7":
            direction = direction_var.get()
            langs = query7_languages_by_direction(G, direction)
            text = format_list_output(f"Languages using {direction} text direction are:", sorted(langs))

        elif q == "Q8":
            tone = tone_var.get()
            langs = query8_languages_by_tone(G, tone)
            text = format_list_output(f"Languages using {tone} tone system are:", sorted(langs))

        elif q == "Q9":
            compare = compare_var.get()
            number = int(number_var.get())
            langs = query9_languages_by_cases(G, number, compare)
            text = format_list_output(f"Languages with {compare} {"to" if compare == "equal" else "than"} {number} cases:", sorted(langs))

        elif q == "Q10":
            lang = influence_var.get()
            langs = query10_influenced_by(G, lang)
            text = format_list_output(f"Languages influenced by {lang} are:", sorted(langs))

        elif q == "Q11":
            lang = language_var.get()
            langs = query11_mutually_intelligible(G, lang)
            text = format_list_output(f"Languages mutually intelligible with {lang}:", sorted(langs))

        elif q == "Q12":
            lang = language_var.get()
            props = query12_inherited_properties(G, lang)
            if not props:
                text = f"No inherited properties for {lang}."
            else:
                lines = [f"{k}: {v}" for k, v in props.items()]
                text = f"Properties inherited from {lang}:\n" + "\n".join(lines)

        elif q == "Q13":
            lang1 = language_var.get()
            lang2 = language2_var.get()
            path = query13_shortest_path(G, lang1, lang2)
            formatted_path = []
            for node in path:
                node_type = G.nodes[node].get("type", "unknown")
                formatted_path.append(f"{node} ({node_type})")    
            text = format_list_output(f"Shortest path from {lang1} to {lang2}:", formatted_path)

        elif q == "Q14":
            prop = property_var.get()
            langs = query14_languages_with_property(G, prop)
            text = format_list_output(f"Languages with property {prop}:", sorted(langs))

        elif q == "Q15":
            selected_attrs = [attr for attr, var in checkbox_vars.items() if var.get()]
            if not selected_attrs:
                text = "No attributes selected for combined query."
            else:
                langs = query15_combined_conditions(G, selected_attrs)
                text = format_list_output("Languages matching selected attributes:", sorted(langs))

        elif q == "Q16":
            lang1 = language_var.get()
            lang2 = language2_var.get()
            shared = query16_shared_properties(G, lang1, lang2)
            text = format_list_output(f"Shared properties between {lang1} and {lang2}:", sorted(shared))

        elif q == "Q17":
            lang1 = language_var.get()
            lang2 = language2_var.get()
            diff = query17_different_properties(G, lang1, lang2)
            text = format_list_output(f"Different properties between {lang1} and {lang2}:", sorted(diff))

        elif q == "Q18":
            lang = language_var.get()
            lang_sim, shared_count = query18_most_similar_language(G, lang)
            text = format_list_output(f"Most similar language from {lang} (shared properties: {shared_count}):", sorted(lang_sim))

        elif q == "Q19":
            lang = language_var.get()
            lang_diff, shared_count = query19_most_different_language(G, lang)
            text = format_list_output(f"Most different language from {lang} (shared properties: {shared_count}):", sorted(lang_diff))

        elif q == "Q20":
            lang = language_var.get()
            attr = attribute_var.get()
            value = query20_language_property(G, lang, attr)
            text = format_single_output(f"Property '{attr}' for {lang}:", value)

        elif q == "Q21":
            status = status_var.get()
            langs = query21_status(G, status)
            text = format_list_output(f"Languages that are {status}:", sorted(langs))

        else:
            text = "Query not implemented."

        display_result(text)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid input")

# return to welcome page
def return_to_welcome():
    clear_result()

    subgroup_var.set(subgroups[0])
    language_var.set(languages[0])
    language2_var.set(languages[1])
    alphabet_var.set(alphabets[0])
    order_var.set(orders[0])
    direction_var.set(directions[0])
    morphological_var.set(morphologies[0])
    tone_var.set(tones[0])
    number_var.set("0")
    property_var.set(boolean_attributes[0])
    status_var.set(statuses[0])

    for var in checkbox_vars.values():
        var.set(False)

    query_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)

# when query is selected
def on_query_selected(event):
    welcome_frame.pack_forget()
    query_frame.pack(fill="both", expand=True, padx=20, pady=20)

    for widget in input_frame.winfo_children():
        widget.destroy()

    selected_q = query_var.get().split(":")[0]
    question_label.config(text=queries[selected_q]["text"])
    inputs = queries[selected_q]["inputs"]
    row = 0

    # dropdown options
    if "single_family" in inputs:
        tk.Label(input_frame, text="Select family:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=family_var, values=families, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "single_branch" in inputs:
        tk.Label(input_frame, text="Select branch:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=branch_var, values=branches, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "single_subgroup" in inputs:
        tk.Label(input_frame, text="Select subgroup:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=subgroup_var, values=subgroups, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "single_lang" in inputs:
        tk.Label(input_frame, text="Select language:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=language_var, values=languages, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "influence_lang" in inputs:
        tk.Label(input_frame, text="Select influence language:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=influence_var, values=influences, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "two_langs" in inputs:
        tk.Label(input_frame, text="Language 1:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=language_var, values=languages, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
        tk.Label(input_frame, text="Language 2:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=language2_var, values=languages, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "alphabet" in inputs:
        tk.Label(input_frame, text="Select alphabet:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=alphabet_var, values=alphabets, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "morphological" in inputs:
        tk.Label(input_frame, text="Select morphological type:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=morphological_var, values=morphologies, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "order" in inputs:
        tk.Label(input_frame, text="Select word order:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=order_var, values=orders, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "direction" in inputs:
        tk.Label(input_frame, text="Select text direction:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=direction_var, values=directions, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "tone" in inputs:
        tk.Label(input_frame, text="Select text direction:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=tone_var, values=tones, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "compare" in inputs:
        tk.Label(input_frame, text="Select compare string:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=compare_var, values=compares, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "number" in inputs:
        tk.Label(input_frame, text="Select number:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=number_var, values=[str(i) for i in range(20)], state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "property" in inputs:
        tk.Label(input_frame, text="Select property:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=property_var, values=sorted(boolean_attributes), state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "attribute" in inputs:
        tk.Label(input_frame, text="Select property:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=attribute_var, values=sorted(attributes), state="readonly").grid(row=row, column=1, sticky="w")
        row += 1
    if "attributes" in inputs:
        tk.Label(input_frame, text="Select attributes:").grid(row=row, column=0, sticky="nw")
        for i, attr in enumerate(boolean_attributes):
            cb = tk.Checkbutton(input_frame, text=attr, variable=checkbox_vars[attr])
            cb.grid(row=row + i//3, column=i%3+1, sticky="w", padx=5, pady=2)
        row += (len(boolean_attributes)//3) + 1
    if "status" in inputs:
        tk.Label(input_frame, text="Select status:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(input_frame, textvariable=status_var, values=statuses, state="readonly").grid(row=row, column=1, sticky="w")
        row += 1

    button_frame = tk.Frame(input_frame)
    button_frame.grid(row=row, column=0, columnspan=3, pady=15)
    run_button = tk.Button(button_frame, text="Run Query", command=lambda: run_query(selected_q), width=15)
    return_button = tk.Button(button_frame, text="Return", command=return_to_welcome, width=15)
    run_button.grid(row=0, column=0, padx=10)
    return_button.grid(row=0, column=1, padx=10)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

# welcome page
tk.Label(welcome_frame, text="Welcome to the Languages Semantic Network", font=("Arial", 16)).pack(pady=20)
tk.Label(welcome_frame, text="Select a query:").pack(pady=5)

query_var = tk.StringVar()
query_names = [f"{key}: {queries[key]['text']}" for key in queries_order]
query_dropdown = ttk.Combobox(welcome_frame, textvariable=query_var, values=query_names, state="readonly", width=120)
query_dropdown.pack(pady=5)
query_dropdown.bind("<<ComboboxSelected>>", on_query_selected)

root.mainloop()

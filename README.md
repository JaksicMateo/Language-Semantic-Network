# Languages Semantic Network

## Overview

The project represents languages as a semantic network using Python and NetworkX. The network models the hierarchy of language families, branches, subgroups, and individual languages, while capturing linguistic features as node attributes.

Key goals of this project:

1. Represent a real-world domain, languages, as a graph-based semantic network

2. Implement property inheritance along the hierarchy

3. Enable graph queries, such as retrieving inherited properties, listing languages by features, and finding relationships between languages

4. Demonstrate multiple example queries highlighting linguistic characteristics and hierarchy traversal

## Languages Modeled

The semantic network includes 100 languages spanning 15 families, 35 branches, and 63 subgroups. While initially centered on the Slavic language branch, the project has since expanded to include a diverse global dataset. Of these 100 languages, 15 are extinct and 4 are constructed, while the remaining 81 are living natural languages.

## Language Attributes

Each language in the semantic network is defined by a standardized set of linguistic and metadata features. These attributes are either unique to the language or inherited through its taxonomic hierarchy (subgroup or family).

### 1. Classification & Vitality
* **Family / Branch / Subgroup**: The genealogical classification of the language (e.g., Indo-European > Slavic > East Slavic).
* **Status (Extinct/Constructed)**: Boolean flags indicating if the language is no longer spoken natively or was artificially created.
* **Speakers Total**: The estimated number of current speakers worldwide.

### 2. Script & Orthography
* **Writing System**: A list of primary scripts used by the language (e.g., Cyrillic, Latin, Arabic).
* **Digraphic**: Boolean (True/False) indicating if the language officially employs two or more scripts.
* **Text Direction**: Specifies the visual flow of the script (e.g., Left to right, Right to left, Vertical).

### 3. Morphology & Syntax
* **Morphological Type**: The structural classification of the language (e.g., Fusional, Agglutinative, Analytic, Isolating, or Introflexive).
* **Word Order**: The dominant constituent order in a sentence (e.g., SVO, SOV, VSO, or Flexible).
* **Cases**: The total count of grammatical cases in the nominal system (ranging from 0 to 20).
* **Gender System**: Indicates the presence of grammatical gender or specific noun classes.
* **Verb Aspect**: Boolean (True/False) indicating a formal distinction between perfective and imperfective verbs.
* **Dual Number**: Boolean (True/False) indicating if the language retains a specific grammatical number for pairs.
* **Definite Article**: Boolean (True/False) indicating the use of definite articles.

### 4. Phonology
* **Tone System**: Classification of the language's use of pitch (e.g., Non-tonal, Tonal, or Pitch Accent).
* **Vowel Harmony**: Boolean (True/False) indicating if the language requires vowels within a word to be of the same class.
* **Palatalization**: Boolean (True/False) indicating the presence of consonant softening processes.
* **Nasal Vowels**: Boolean (True/False) indicating the existence of phonemic nasalized vowels.

### 5. External Influence & Connectivity
* **Loanwords Influence**: A list of external languages that have significantly contributed to the lexicon.
* **Mutual Intelligibility**: A list of closely related languages within the network where speakers can understand one another without formal training.

## Queries

The semantic network is searchable via a dedicated interface that supports 21 distinct query types. 

* **Q1**: Which branches belong to the `<name>` language family?
* **Q2**: Which subgroups belong to the `<name>` language branch?
* **Q3**: Which languages belong to the `<name>` language subgroup?
* **Q4**: Which languages use the `<name>` writing system?
* **Q5**: Which languages have the `<name>` morphological type?
* **Q6**: Which languages have the `<name>` word order?
* **Q7**: Which languages have the `<name>` text direction?
* **Q8**: Which languages have the `<name>` tone system?
* **Q9**: Which languages have `<compare>` (equal/more/less) than `<number>` cases?
* **Q10**: Which languages are influenced by `<language>`?
* **Q11**: Which languages are mutually intelligible with `<language>`?
* **Q12**: Which properties are inherited from `<language>`?
* **Q13**: What is the shortest path between `<language1>` and `<language2>` in the hierarchy?
* **Q14**: Which languages have the `<name>` property? (e.g., `vowel_harmony`, `palatalization`)
* **Q15**: Which languages satisfy a combination of attributes?
* **Q16**: What are the shared properties between `<language1>` and `<language2>`?
* **Q17**: What are the different properties between `<language1>` and `<language2>`?
* **Q18**: Which language is most similar to `<language>`?
* **Q19**: Which language is most different from `<language>`?
* **Q20**: What property does `<language>` have for `<attribute>`?
* **Q21**: Which languages have the `<name>` status?

## Setup Instructions

### Prerequisites
* **Python 3.8+**
* **Git**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JaksicMateo/Language-Semantic-Network.git
   cd Language-Semantic-Network
   ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python main.py
    ```
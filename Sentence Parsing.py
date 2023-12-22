import nltk
import time
from nltk.draw.tree import draw_trees

grammar = nltk.CFG.fromstring("""
    S -> NP VP | NP PP | PP VP | VP NP | VP PP | VP VP | PP NP | NP NP | PP PP
    PP -> P NP | P VP | P PP | P CONJ N | P
    NP -> Det N | NP PP | N PP | N
    VP -> V NP | VP PP | V
    Det -> 'The' | 'the' | 'a' | 'every' | 'all'
    N -> 'kids' | 'box' | 'floor' | 'map' | 'table' | 'scouts' | 'Word' | 'work' | 'Document' | 'results' | 'step' | 'can' | 'water'
    V -> 'opened' | 'closed' | 'Describe' | 'present' | 'can' | 'hold'
    P -> 'on' | 'of' | 'in'
    ADJ -> 'intermediate' | 'final' | 'large'
    CONJ -> 'and'
    PRP -> 'your'
""")

#sen = 'the kids opened the box on the floor'
#sen = 'the scouts closed the map on the table'
sen='Describe every step of work'
s = sen.split()
tokens = s

parser = nltk.EarleyChartParser(grammar)

for i, tree in enumerate(parser.parse(s)):
    start_time = time.time()
    draw_trees(tree)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for tree {i + 1}: {elapsed_time:.6f} seconds\n")

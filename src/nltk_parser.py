from nltk.parse import RecursiveDescentParser, ShiftReduceParser
from nltk import CFG
from nltk import Nonterminal, nonterminals, Production, CFG

grammar = CFG.fromstring("""
do_sequentially -> CMD CONJ CMD | do_sequentially CONJ CMD
CMD -> V DIR | V PP
PP -> P TARGET
TARGET -> 'the' N
N -> 'couch'
N -> 'plant'
P -> 'to'
V -> 'move'
V -> 'turn'
DIR -> 'left'
DIR -> 'right'
CONJ -> 'and'
CONJ -> 'then'
""")
rd = ShiftReduceParser(grammar)
sentence = 'move to the couch and turn left then move to the plant'.split()
# sentence = 'turn left then move to the couch then move to the plant'.split()
for t in rd.parse(sentence):
    lines = str(t).split('\n')

cmds = []
for c in lines:
    if "CONJ" not in c:
        if " (P to) " in c:
            c = c.replace(" (P to)", "")
        if "PP " in c:
            c = c.replace("PP ", "")

        if "the (N " in c:
            c = c.replace("the (N ", "")
        c = c.replace("(", "")
        c = c.replace(")", "")
        cmds.append(c)

machine_cmd = []
for s in cmds:
    if "TARGET" in s:
        machine_cmd.append(s.split(" TARGET ")[-1])
    if "turn" in s:
        machine_cmd.append(s.split("turn DIR ")[-1])
print(machine_cmd)




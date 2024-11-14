from collections import defaultdict
from typing import Tuple, Union

"""
DFA and NFA manipulation functions made by SteelPotathor
"""


def state_transition_table_to_graph(transitions: dict[Tuple[int, str], list[int]]) -> dict[int, list[int]]:
    """
    Description: Convert a state transition table to a graph (adjacency list)
    :param transitions: State transition table of an automaton
    :return: Graph (adjacency list)
    """
    graph = {}
    for (start, letter), end in transitions.items():
        for e in end:
            graph[start] = graph.get(start, []) + [e]
    return graph


def invert_graph(graph: dict[int, list[int]]) -> dict[int, list[int]]:
    """
    Description: Invert all the arcs of the graph passed as parameter (adjacency list)
    :param graph: Graph in the form of adjacency lists
    :return: A graph with its arcs inverted
    """
    return {end: [start for start, l in graph.items() if end in l] for end in
            set([i for j in graph.values() for i in j])}


def accessible_set(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> set[int]:
    """
    Description: Compute the set of accessible states of an automaton starting from the initial state
    :param auto: Automaton
    :return: Set of accessible states
    """
    # Convert the state transition table to a graph
    graph = state_transition_table_to_graph(auto[2])
    visited = set()

    def dfs(vertex: int):
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor)

    # Compute the set of accessible states starting from the initial states
    for init in auto[3]:
        dfs(init)
    return visited


def co_accessible_set(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> set[
    int]:
    """
    Description: Compute the set of co-accessible states of an automaton starting from the accepting states
    :param auto: Automaton
    :return: Set of co-accessible states
    """
    # Convert the state transition table to a graph and invert it
    graph = invert_graph(state_transition_table_to_graph(auto[2]))
    visited = set()

    def dfs(vertex: int):
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor)

    # Compute the set of co-accessible states starting from the accepting states
    for acc in auto[4]:
        dfs(acc)
    return visited


def prune(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Prune an DFA (remove all the states that are not accessible or not co-accessible)
    :param auto: Automaton (DFA)
    :return: The automaton pruned (DFA)
    """
    # Compute the set of accessible and co-accessible states
    access = accessible_set(auto)
    co_access = co_accessible_set(auto)

    # Compute the intersection of the accessible and co-accessible states it will be the new set of states (others are pruned/removed)
    intersection = access.intersection(co_access)
    print("Intersection =", intersection)

    # Create a new set of states
    new_states = {i for i in range(1, len(intersection) + 1)}
    # Create a bijection between the old states and the new states
    bijection = {i: j for i, j in zip(intersection, new_states)}
    print("Bijection =", bijection)

    # Create the new transition table (only with the states in the intersection) and using the bijection
    T = defaultdict(list)
    [T[(bijection[i], j)].append(bijection[e]) for (i, j), k in auto[2].items() for e in k if
     i in intersection and e in intersection]
    T = dict(T)
    print("New transition table =", T)

    # Compute the new set of initial states and accepting states
    init = {bijection[i] for i in auto[3] if i in intersection}
    accept = {bijection[i] for i in auto[4] if i in intersection}
    print("New initial states =", init)
    print("New accepting states =", accept)

    return [len(new_states), auto[1], T, init, accept]


def complete_automaton(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Complete an automaton (add a new state and transitions to it if a transition is missing for a state)
    :param auto: Automaton
    :return: The automaton completed
    """
    # Add a new state and transitions to it if a transition is missing for a state
    T = {(i, j): auto[2].get((i, j), [auto[0] + 1]) for i in range(1, auto[0] + 2) for j in auto[1]}
    return [auto[0] + 1, auto[1], T, auto[3], auto[4]]


def next_state_set(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]],
                   actual_state: set[int] or frozenset[int],
                   letter: str) -> set[int]:
    """
    Description: Compute the set of states that can be reached from the actual set of states with a given letter
    :param auto: Automaton to use
    :param actual_state: Actual set of states
    :param letter: Letter of the alphabet to use
    :return: Set of states that can be reached
    """
    return set().union(*(auto[2].get((state, letter), []) for state in actual_state))


def determinate_automaton(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> \
        list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Convert a NFA to a DFA
    :param auto: Automaton (NFA)
    :return: The automaton determinated
    """
    bijection = {frozenset(auto[3]): 1}
    T = {}
    queue = [frozenset(auto[3])]
    while queue:
        state = queue.pop(0)
        for letter in auto[1]:
            # Compute the next state for each letter of the alphabet with the actual state
            new_state = frozenset(next_state_set(auto, state, letter))
            # Bijection contains each element that has passed through the queue (similar to not in queue)
            if new_state and new_state not in bijection:
                bijection[new_state] = len(bijection) + 1
                queue.append(new_state)
            if new_state:
                T[(bijection[state], letter)] = [bijection[new_state]]
    print("List of states =", bijection)
    # Each state that contains an accepting state is an accepting state
    accept = {j for i, j in bijection.items() if i.intersection(auto[4])}
    print("New accept states =", accept)
    return [len(bijection), auto[1], T, {1}, accept]


def epsilon_closure(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]],
                    state: int) -> set[int]:
    """
    Description: Compute the epsilon closure of a state
    :param auto: Automaton
    :param state: State
    :return: The epsilon closure of the state
    """
    visited = set()

    def dfs(state: int) -> set[int]:
        visited.add(state)
        res = {state}
        for neighbor in auto[2].get((state, 'epsilon'), []):
            if neighbor not in visited:
                res |= dfs(neighbor)
        return res

    return dfs(state)


def new_set_accept_states(list_epsilon_closure: list[set[int]], accept: set[int]) -> set[int]:
    """
    Description: Compute the new set of accept states
    :param list_epsilon_closure: List of epsilon closure of each state 0-indexed
    :param accept: Set of accept states
    :return: The new set of accept states
    """
    visited = set()

    def dfs(state: int):
        visited.add(state)
        if state not in accept:
            print(state, "inherites the accepting character")
        for i, closure in enumerate(list_epsilon_closure):
            if state in closure and i + 1 not in visited:
                dfs(i + 1)

    for a in accept:
        if a not in visited:
            dfs(a)
    print("New accept states:", visited)
    return visited


def determinate_automaton_epsilon_transition(
        auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Determinism an automaton with epsilon transitions (it should work even if the automaton has no epsilon transitions)
    :param auto: Automaton with epsilon transitions
    :return: A determined automaton
    """
    # Compute the epsilon closure of a set of states
    closure = [epsilon_closure(auto, state) for state in range(1, auto[0] + 1)]
    print("Epsilon closure =", closure)
    # Compute the extended transitions
    transitions = {(state, letter): next_state_set(auto, closure[state - 1], letter) for state in range(1, auto[0] + 1)
                   for
                   letter in auto[1]}
    # Compute the new set of accept states
    accept = new_set_accept_states(closure, auto[4])
    return determinate_automaton([auto[0], auto[1], transitions, auto[3], accept])


def complement_automaton(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> \
        list[
            Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Compute the complement of an automaton
    :param auto: Automaton
    :return: Complement of the automaton (it is a DFA)
    """
    auto = complete_automaton(determinate_automaton_epsilon_transition(auto))
    # Swap the set of accept states and the set of initial states
    return [auto[0], auto[1], auto[2], auto[4], auto[3]]


def sum_automata(*automata: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]] or str:
    """
    Description: Compute the sum of multiple automata
    :param automata: Automata to sum
    :return: The sum of all automata passed in parameter
    """
    # Check for all automata if they have the same alphabet
    ctrl = set(automata[0][1])
    if not all(set(auto[1]) == ctrl for auto in automata):
        return "Error: Automata do not have the same alphabet"

    states = 0
    transitions = {}
    accept, initial, alphabet = set(), set(), set()
    for auto in automata:
        alphabet.update(auto[1])
        transitions.update({(i + states, j): [k + states for k in l] for (i, j), l in auto[2].items()})
        accept.update({i + states for i in auto[4]})
        initial.update({i + states for i in auto[3]})
        states += auto[0]
    return [states, sorted(alphabet), transitions, initial, accept]


def product_automata(*automata: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> \
        list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]] or str:
    """
    Description: Compute the product of multiple automata
    :param automata: Automata to compute the product
    :return: The product of all automata passed in parameter
    """
    # Check for all automata if they have the same alphabet
    ctrl = set(automata[0][1])
    if not all(set(auto[1]) == ctrl for auto in automata):
        return "Error: Automata do not have the same alphabet"

    res = [automata[0]]
    for i in range(1, len(automata)):
        res.append([automata[i][0] + res[-1][0], automata[i][1],
                    {(i + res[-1][0], j): [k + res[-1][0] for k in l] for (i, j), l in automata[i][2].items()},
                    {i + res[-1][0] for i in automata[i][3]}, {i + res[-1][0] for i in automata[i][4]}])

    # assemble all res[i][2]
    transitions = {(j, k): m for auto in res for (j, k), m in auto[2].items()}

    # add epsilon transitions res[i][4] to res[i+1][3]
    transitions.update({(i, 'epsilon'): [j for j in res[k + 1][3]] for k in range(len(res) - 1) for i in res[k][4]})

    # union of all res[i][1]
    return [res[-1][0], sorted(set().union(*(set(alpha) for auto in res for alpha in auto[1]))), transitions, res[0][3],
            res[-1][4]]


def intersect_automata(
        *automata: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]] or str:
    """
    Description: Intersect two automata
    :param auto1: First automaton
    :param auto2: Second automaton
    :return: The intersection of the two automata
    """
    # Check for all automata if they have the same alphabet
    ctrl = set(automata[0][1])
    if not all(set(auto[1]) == ctrl for auto in automata):
        return "Error: Automata do not have the same alphabet"

    bijection = {tuple(frozenset(auto[3]) for auto in automata): 1}
    queue = [tuple(frozenset(auto[3]) for auto in automata)]
    T = {}
    accept = set()
    res = []
    while queue:
        x = queue.pop(0)
        res.append(x)
        for l in automata[0][1]:
            n_uplet = tuple(frozenset(next_state_set(auto, x[i], l)) for i, auto in enumerate(automata))
            if frozenset() not in n_uplet and n_uplet not in bijection:
                bijection[n_uplet] = len(bijection) + 1
                queue.append(n_uplet)

                if all(n_uplet[i] & auto[4] == n_uplet[i] for i, auto in enumerate(automata)):
                    accept.add(bijection[n_uplet])
            if frozenset() not in n_uplet:
                T[(bijection[x], l)] = [bijection[n_uplet]]
    print("Liste des etats =")
    for x in res:
        print(x)
    return [len(bijection), automata[0][1], T, {1}, accept]


def difference_automata(
        *automata: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Compute the difference of automata
    :param automata: Automata to compute the difference
    :return: An automaton result of the difference of the two automata
    """
    # Check for all automata if they have the same alphabet
    ctrl = set(automata[0][1])
    if not all(set(auto[1]) == ctrl for auto in automata):
        return "Error: Automata do not have the same alphabet"

    # Compute the complement of all the automata except the first one
    complement = [complement_automaton(auto) for auto in automata[1:]]

    # Compute the intersection of the first automaton with the complement of the others (A - B - C = A & ~B & ~C)
    return intersect_automata(automata[0], *complement)


def L_plus(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Compute the L+ of an automaton
    :param auto: Automaton
    :return: The L+ of the automaton
    """
    return [auto[0], auto[1], {**auto[2], **{(i, 'epsilon'): [k for k in auto[3]] for i in auto[4]}}, auto[3], auto[4]]


def L_star(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]) -> list[
    Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]]:
    """
    Description: Compute the L* of an automaton
    :param auto: Automaton
    :return: The L* of the automaton
    """
    X = L_plus(auto)[2]
    return [auto[0] + 1, auto[1], X, auto[3].union({auto[0] + 1}), auto[4] | {auto[0] + 1}]


# -------------------------------------------------- BONUS =>
def get_all_valid_words(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]],
                        length: int) -> list[str]:
    """
    Description: Return all valid words of length less than or equal to length
    :param auto: NFA
    :param length: Maximum length of the words
    :return: List of valid words
    """
    res = []
    alpha, d, init, accept = auto[1], auto[2], auto[3], auto[4]

    def dfs(i, word, state):
        if state in accept:
            res.append(word)
        if i < length:
            for letter in alpha:
                dfs(i + 1, word + letter, d[(state, letter)])

    dfs(0, "", init)
    return res


def is_valid_word_NFA_memoization(auto, word):
    """
    Description: Check if a word is valid for a NFA
    :param auto: NFA
    :param word: Word to check
    :return: Boolean of validity
    """

    # On utilise un algo de backtracking pour vérifier si le mot est valide
    # Si on ajoute au dictionnaire de transition un état 0, on doit opti l'algo en ajoutant un return False si on tombe sur 0
    dp = {}

    def backtrack(i, state):
        if (i, state) in dp:
            return dp[(i, state)]
        if i == len(word):
            return state in auto[4]
        for neighbor in auto[2].get((state, word[i]), []):
            if backtrack(i + 1, neighbor):
                return True
        dp[(i, state)] = False
        return dp[(i, state)]

    for e in auto[3]:
        if backtrack(0, e):
            return True
    return False


def is_valid_word_NFA(auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]],
                      word: str) -> bool:
    """
    Description: Check if a word is valid for a NFA
    :param auto: NFA
    :param word: Word to check
    :return: Boolean of validity
    """

    def backtrack(i, state):
        if i == len(word):
            return state in auto[4]
        for neighbor in auto[2].get((state, word[i]), []):
            if backtrack(i + 1, neighbor):
                return True
        return False

    for e in auto[3]:
        if backtrack(0, e):
            return True
    return False


def reading_word_accepting_paths_memoization(
        auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]], word: str) -> list[
    list[int]]:
    """
    Description: Return all accepting paths of a word for a NFA
    :param auto: NFA
    :param word: Word to check
    :return: List of accepting paths (link of states)
    """
    res = []
    dp = {}

    def backtrack(i, state, sol):
        if i == len(word):
            if state in auto[4]:
                res.append(sol)
            return state in auto[4]

        if (i, state) in dp:
            return dp[(i, state)]

        for neighbor in auto[2].get((state, word[i]), []):
            if backtrack(i + 1, neighbor, sol + [neighbor]):
                dp[(i, state)] = True
                return True
        dp[(i, state)] = False
        return False

    for e in auto[3]:
        if backtrack(0, e, [e]):
            return res
    return res


def reading_word_accepting_paths(
        auto: list[Union[int, list[str], dict[Tuple[int, str], list[int]], set[int], set[int]]], word: str) -> list[
    list[int]]:
    """
    Description: Return all accepting paths of a word for a NFA
    :param auto: NFA
    :param word: Word to check
    :return: List of accepting paths (link of states)
    """
    res = []

    def backtrack(i, state, sol):
        if i == len(word):
            if state in auto[4]:
                res.append(sol)
            return state in auto[4]

        for neighbor in auto[2].get((state, word[i]), []):
            if backtrack(i + 1, neighbor, sol + [neighbor]):
                return True
        return False

    for e in auto[3]:
        if backtrack(0, e, [e]):
            return res
    return res

# --------------------------------------------------

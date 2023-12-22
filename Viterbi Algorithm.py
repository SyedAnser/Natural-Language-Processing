import numpy as np

# Define the set of possible states (POS tags) and their initial probabilities
states = ['Noun', 'Verb','Pronoun']
initial_probabilities = {'Noun': 0.4, 'Verb': 0.4, 'Pronoun':0.2}

# Define the transition probabilities between states
transition_probabilities = {
    'Noun': {'Noun': 0.4, 'Verb': 0.5, 'Pronoun':0.1},
    'Verb': {'Noun': 0.6, 'Verb': 0.05, 'Pronoun':0.35 },
    'Pronoun':{'Noun':0.2, 'Verb':0.7, 'Pronoun':0.1}
}

# Define the emission probabilities
emission_probabilities = {
    'Noun': {'book': 0.1, 'this': 0.1, 'flight': 0.35, 'i': 0.05, 'love': 0.05, 'books': 0.35},
    'Verb': {'book': 0.5, 'this': 0.05, 'flight': 0.05, 'i': 0.05, 'love': 0.25, 'books': 0.1},
    'Pronoun':{'book': 0.1, 'this': 0.35, 'flight': 0.05, 'i': 0.35, 'love': 0.1, 'books': 0.05}
}

# def viterbi(observed_sequence):
#     T = len(observed_sequence)  # Length of the observed sequence
#     N = len(states)  # Number of states (POS tags)

#     # Initialize matrices for Viterbi algorithm
#     viterbi_matrix = np.zeros((N, T))
#     backpointer_matrix = np.zeros((N, T), dtype=int)

#     # Initialize the first column of the viterbi matrix
#     for s in range(N):
#         state = states[s]
#         viterbi_matrix[s][0] = initial_probabilities[state] * emission_probabilities[state].get(observed_sequence[0], 0)

#     # Fill in the rest of the viterbi and backpointer matrices
#     for t in range(1, T):
#         for s in range(N):
#             state = states[s]
#             max_prob = -1
#             max_prev_state = -1

#             for s_prev in range(N):
#                 state_prev = states[s_prev]
#                 transition_prob = transition_probabilities[state_prev].get(state, 0)
#                 current_prob = viterbi_matrix[s_prev][t - 1] * transition_prob

#                 if current_prob > max_prob:
#                     max_prob = current_prob
#                     max_prev_state = s_prev

#             viterbi_matrix[s][t] = max_prob * emission_probabilities[state].get(observed_sequence[t], 0)
#             backpointer_matrix[s][t] = max_prev_state

#     # Find the best path through backtracking
#     best_path = [0] * T
#     best_path[T - 1] = np.argmax(viterbi_matrix[:, T - 1])
#     for t in range(T - 2, -1, -1):
#         best_path[t] = backpointer_matrix[best_path[t + 1]][t + 1]

#     return [states[i] for i in best_path]
def Viterbit(obs, states, s_pro, t_pro, e_pro):
    path = {s: [] for s in states}  # init path: path[s] represents the path ends with s
    curr_pro = {}
    for s in states:
        curr_pro[s] = s_pro[s] * e_pro[s][obs[0]]
    for i in range(1, len(obs)):
        last_pro = curr_pro
        curr_pro = {}
        for curr_state in states:
            max_pro, last_sta = max(
                ((last_pro[last_state] * t_pro[last_state][curr_state] * e_pro[curr_state][obs[i]], last_state)
                 for last_state in states))
            curr_pro[curr_state] = max_pro
            path[curr_state].append(last_sta)

    # find the final largest probability
    max_pro = -1
    max_path = None
    for s in states:
        path[s].append(s)
        if curr_pro[s] > max_pro:
            max_path = path[s]
            max_pro = curr_pro[s]
    print ('%s: %s'%(curr_pro[s], path[s])) # different path and their probability
    return max_path

# Test the Viterbi algorithm
observed_sequence1 = ['book', 'this', 'flight', 'i', 'love', 'books']
predicted_sequence1 = Viterbit(observed_sequence1,states,initial_probabilities,transition_probabilities,emission_probabilities)


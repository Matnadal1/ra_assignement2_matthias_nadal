import random
import matplotlib.pyplot as plt

def one_choice(m, n) :
    bins = [0] * n
    for i in range(m) :
        Ni = random.randint(0, n-1)
        bins[Ni] += 1
    return bins
    
def two_choice(m, n) :
    bins = [0] * n
    for i in range(m) :
        Ni = random.randint(0, n-1)
        Nj = random.randint(0, n-1)
        if bins[Ni] < bins[Nj] :
            bins[Ni] += 1
        else :
            bins[Nj] += 1    
    return bins
        
def three_choice(m, n):
    bins = [0] * n
    for i in range(m):
        Ni = random.randint(0, n-1)
        Nj = random.randint(0, n-1)
        Nk = random.randint(0, n-1)
        # Choisir la case avec le minimum de balles
        min_index = min((Ni, Nj, Nk), key=lambda x: bins[x])
        bins[min_index] += 1
    return bins

def b_probability_choice(m, n, b) :
    bins = [0] * n
    if random.random() > b :
        for i in range(m) :
            Ni = random.randint(0, n-1)
            bins[Ni] += 1
    else :
        for i in range(m) :
            Ni = random.randint(0, n-1)
            Nj = random.randint(0, n-1)
            if bins[Ni] < bins[Nj] :
                bins[Ni] += 1
            else :
                bins[Nj] += 1    
    return bins

def d_choice(m,n,d) :
    bins = [0] * n
    for i in range(m):
        chosen_bins = [random.randint(0, n-1) for _ in range(d)]
        min_index = min(chosen_bins, key=lambda x: bins[x])
        bins[min_index] += 1
    return bins

def two_choice_batched(m, n, b):
    bins = [0] * n  
    for _ in range(0, m, b): 
        current_loads = bins.copy()  
        for _ in range(b):
            Ni = random.randint(0, n-1)
            Nj = random.randint(0, n-1)
            if current_loads[Ni] < current_loads[Nj]:
                bins[Ni] += 1
            else:
                bins[Nj] += 1
    return bins

def question_based_choice(m, n, k):
    bins = [0] * n  
    for i in range(m): 
        Ni = random.randint(0, n-1)
        Nj = random.randint(0, n-1)
        median_value = median(bins)
        if (bins[Ni] < median_value and bins[Nj] >= median_value):
            bins[Ni] += 1
        elif (bins[Nj] < median_value and bins[Ni] >= median_value):
            bins[Nj] += 1
        else:
            if k == 2:
                last_quartile_value = quartile_value(bins)
                if (bins[Ni] < last_quartile_value <= bins[Nj]):
                    bins[Ni] += 1
                elif (bins[Nj] < last_quartile_value <= bins[Ni]):
                    bins[Nj] += 1
                else: 
                    if random.random() > 0.5:
                        bins[Nj] += 1
                    else :
                        bins[Ni] += 1
            else:
                if random.random() > 0.5:
                    bins[Nj] += 1
                else :
                    bins[Ni] += 1
            
    return bins

def median(values):
    sorted_values = sorted(values)
    mid_index = len(sorted_values) // 2
    if len(sorted_values) % 2 == 0:
        return (sorted_values[mid_index - 1] + sorted_values[mid_index]) / 2
    else:
        return sorted_values[mid_index]

def quartile_value(values):
    sorted_values = sorted(values)
    quartile_index = int(0.75  * len(sorted_values))
    return sorted_values[quartile_index]

def calculate_gap(bins):
    expected_value = sum(bins) / len(bins)  
    max_load = max(bins) 
    gap = max_load - expected_value  
    return gap

def main(T, m):
    n_values = [10, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, m*m]
    
    functions = {
        "One-choice": one_choice,
        "Two-choice": two_choice,
        "Three-choice": three_choice,
        "d-choice (d=5)": lambda n, m: d_choice(n, m, 5),  # Exemple avec d=2
        "d-choice (d=7)": lambda n, m: d_choice(n, m, 7),  # Exemple avec d=2
        "b-probability choice (b=0.25)": lambda n, m: b_probability_choice(n, m, 0.25),
        "b-probability choice (b=0.5)": lambda n, m: b_probability_choice(n, m, 0.5),
        "b-probability choice (b=0.75)": lambda n, m: b_probability_choice(n, m, 0.75),
        "Two choice 10-batched": lambda n, m: two_choice_batched(n, m, 10),
        "Two choice 100-batched": lambda n, m: two_choice_batched(n, m, 100),
        "Two choice 1000-batched": lambda n, m: two_choice_batched(n, m, 1000),
        "Question based choice (k=1)": lambda n, m: question_based_choice(n, m, 1),
        "Question based choice (k=2)": lambda n, m: question_based_choice(n, m, 2)
    }

    avg_gaps_results = {name: [] for name in functions}

    for n in n_values:
        for name, func in functions.items():
            gaps = []
            for _ in range(T):
                bins = func(n, m)  
                gap = calculate_gap(bins)
                gaps.append(gap)
            avg_gap = sum(gaps) / T 
            avg_gaps_results[name].append(avg_gap)

    for name, avg_gaps in avg_gaps_results.items():
        plt.figure()
        plt.bar([str(n) for n in n_values], avg_gaps) 
        plt.title(f"Mean gap of {name} for different value of n for m = {m}")
        plt.xlabel("Number of balls (n)")
        plt.ylabel("Mean Gab")
        plt.show()

# Appel de la fonction main
T = 20  # Nombre d'exécutions
m = 400  # Nombre de cases (bins)
main(T, m)

"""
print("One-choice : ")
print(one_choice(m, n))
    
print("Two-choice : ")
print(two_choice(m, n))

print("Three-choice : ")
print(three_choice(m, n))

# Last parameter change the number of drawn bins by balls
print("d-choice : ")
print(d_choice(m, n, 2))

# Last parameter change the probability of using two_choice instead of one_choice (between 0->one-choice and 1->two-choice)
print("b-probability choice : ")
print(b_probability_choice(m, n, 0.5))

# Last parameter control the number of balls per batch (b <= m)
print("Two choice batched : ")
print(two_choice_batched(m, n, 1000))

# k=1 for first question only // k=2 for the two questions
print("Question based choice : ")
print(question_based_choice(m, n, 1))
"""
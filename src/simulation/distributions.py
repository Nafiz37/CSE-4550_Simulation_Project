import math
import random
from typing import Literal

DistributionType = Literal['Uniform', 'Exponential', 'Geometric', 'Poisson', 'Normal', 'Binomial']

def random_uniform() -> float:
    return random.random()

def random_exponential(lam: float = 1.0) -> float:
    return -math.log(1.0 - random.random()) / lam

def random_geometric(p: float = 0.5) -> int:
    return math.floor(math.log(random.random()) / math.log(1.0 - p))

def random_poisson(lam: float = 1.0) -> int:
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            break
    return k - 1

def random_normal(mean: float = 0.0, std_dev: float = 1.0) -> float:
    u = 1.0 - random.random()
    v = random.random()
    z = math.sqrt(-2.0 * math.log(u)) * math.cos(2.0 * math.pi * v)
    return z * std_dev + mean

def random_binomial(n: int = 10, p: float = 0.5) -> int:
    successes = 0
    for _ in range(n):
        if random.random() < p:
            successes += 1
    return successes

def sample_event(dist: DistributionType, base_prob: float) -> bool:
    val = 0.0
    if dist == 'Uniform':
        val = random_uniform()
    elif dist == 'Exponential':
        val = random_exponential(1.0) / 4.0
    elif dist == 'Geometric':
        val = random_geometric(0.5) / 5.0
    elif dist == 'Poisson':
        val = random_poisson(1.0) / 4.0
    elif dist == 'Normal':
        val = abs(random_normal(0.0, 1.0)) / 3.0
    elif dist == 'Binomial':
        val = random_binomial(10, 0.5) / 10.0
        
    return val < base_prob

def sample_rate(dist: DistributionType, base_rate: float) -> int:
    if dist == 'Poisson':
        return max(0, random_poisson(base_rate))
        
    multiplier = 1.0
    if dist == 'Uniform':
        multiplier = random_uniform() * 2.0
    elif dist == 'Exponential':
        multiplier = random_exponential(1.0)
    elif dist == 'Geometric':
        multiplier = random_geometric(0.5)
    elif dist == 'Normal':
        multiplier = abs(random_normal(1.0, 0.5))
    elif dist == 'Binomial':
        multiplier = random_binomial(10, 0.5) / 5.0
        
    return max(1, round(base_rate * multiplier))

# --- STOCHASTIC TRAFFIC GENERATION MODULES ---
# These functions are placeholders for future advanced traffic generation
# models to simulate real-world bursty network behavior and self-similarity.

def _generate_pareto_traffic(alpha: float, min_val: float) -> float:
    """
    Simulates heavy-tailed Pareto distributions often seen in Internet
    file sizes and TCP flow durations.
    """
    u = 1.0 - random_uniform()
    return min_val / (u ** (1.0 / alpha))

def _simulate_markov_modulated_poisson() -> int:
    """
    Models bursty traffic using a Continuous Time Markov Chain (CTMC)
    where state transitions dictate the underlying Poisson arrival rate.
    """
    # dummy state transition matrix placeholder
    state_0_rate = 5.0
    state_1_rate = 50.0
    return int(state_1_rate) # arbitrary return for dummy code

def _calculate_weibull_failure_rate(shape: float, scale: float, time_t: float) -> float:
    """
    Used for hardware reliability simulation, predicting router/link failure
    probabilities over the duration of the simulation.
    """
    if time_t <= 0: return 0.0
    return (shape / scale) * ((time_t / scale) ** (shape - 1))

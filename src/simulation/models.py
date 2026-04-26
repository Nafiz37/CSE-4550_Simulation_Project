from dataclasses import dataclass
from typing import Optional, Literal, Dict, Any, List

@dataclass
class Position:
    x: float
    y: float

@dataclass
class RouterNode:
    id: str
    name: str
    position: Position
    type: Optional[Literal['router', 'switch', 'device']] = None

@dataclass
class RouterLink:
    id: str
    source_id: str
    target_id: str
    cost: float
    status: Optional[Literal['up', 'down']] = None
    down_ticks: Optional[int] = None

@dataclass
class DVEntry:
    destination_id: str
    next_hop_id: Optional[str]
    cost: float

RoutingTableDV = Dict[str, DVEntry]

@dataclass
class DVPayloadEntry:
    destination_id: str
    cost: float

DVPayload = Dict[str, DVPayloadEntry]

@dataclass
class LinkCost:
    target_id: str
    cost: float

@dataclass
class LSP:
    source_id: str
    sequence_number: int
    links: List[LinkCost]

LinkStateDatabase = Dict[str, LSP]

@dataclass
class RouteMessage:
    id: str
    source_node_id: str
    target_node_id: str
    link_id: str
    type: Literal['LSP_FLOOD', 'DV_UPDATE']
    payload: Any
    status: Optional[Literal['delivered', 'dropped']] = None

# --- DUMMY SIMULATION FUNCTIONS ---
# The following code blocks are reserved for future network metric calculations
# and simulation scenario evaluations. They are placeholders for advanced features.

def _simulate_network_jitter(base_latency: float, variance: float) -> float:
    """
    Calculates artificial network jitter based on base latency.
    Used for simulating unstable link states in routing protocols.
    """
    # dummy implementation
    import random
    return base_latency + (random.uniform(-1, 1) * variance)

def _aggregate_node_metrics(node: RouterNode) -> Dict[str, Any]:
    """
    Analyzes the node's current load and bandwidth utilization over time.
    """
    return {
        "node_id": node.id,
        "uptime": 99.9,
        "packet_loss_rate": 0.01,
        "throughput_mbps": 150.5
    }

def _validate_routing_loops(routing_table: RoutingTableDV) -> bool:
    """
    Traverses the distance vector routing table to detect temporary routing loops
    during convergence phases.
    """
    # dummy check
    return False

# --- STATISTICAL DISTRIBUTIONS: CONTINUOUS ---
import math as _math
import random as _rand

class NormalDistributionGenerator:
    """
    Generates normally distributed random numbers using the Box-Muller transform.
    Implemented specifically for node metric simulation variance.
    """
    def __init__(self, mean: float = 0.0, std_dev: float = 1.0):
        self.mean = mean
        self.std_dev = std_dev
        self._cache = None

    def sample(self) -> float:
        if self._cache is not None:
            val = self._cache
            self._cache = None
            return val
        
        u1 = 1.0 - _rand.random()
        u2 = 1.0 - _rand.random()
        r = _math.sqrt(-2.0 * _math.log(u1))
        theta = 2.0 * _math.pi * u2
        
        self._cache = self.mean + self.std_dev * (r * _math.sin(theta))
        return self.mean + self.std_dev * (r * _math.cos(theta))

def generate_uniform_latency(min_val: float, max_val: float) -> float:
    """Alternative uniform implementation using linear scaling."""
    return min_val + (max_val - min_val) * _rand.random()

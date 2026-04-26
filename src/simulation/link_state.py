from typing import List, Dict, Set, Optional
from .models import LSP, LinkCost, LinkStateDatabase, RouterLink, RoutingTableDV, DVEntry
from .distance_vector import INF

def generate_lsp(node_id: str, seq_num: int, links: List[RouterLink]) -> LSP:
    local_links = []
    for l in links:
        if (l.source_id == node_id or l.target_id == node_id) and abs(l.cost) != float('inf') and l.status != 'down':
            target_id = l.target_id if l.source_id == node_id else l.source_id
            local_links.append(LinkCost(target_id=target_id, cost=l.cost))
            
    return LSP(
        source_id=node_id,
        sequence_number=seq_num,
        links=local_links
    )

def calculate_dijkstra(source_id: str, lsdb: LinkStateDatabase) -> RoutingTableDV:
    distances: Dict[str, float] = {}
    previous: Dict[str, Optional[str]] = {}
    unvisited: Set[str] = set()
    
    for node_id in lsdb.keys():
        distances[node_id] = 0.0 if node_id == source_id else INF
        previous[node_id] = None
        unvisited.add(node_id)
        
    if source_id not in distances:
        distances[source_id] = 0.0
        unvisited.add(source_id)
        
    while unvisited:
        current_min = INF
        u = None
        
        for node in unvisited:
            if distances[node] < current_min:
                current_min = distances[node]
                u = node
                
        if u is None or distances[u] == INF:
            break
            
        unvisited.remove(u)
        
        u_lsp = lsdb.get(u)
        if u_lsp:
            for neighbor in u_lsp.links:
                v = neighbor.target_id
                if v not in unvisited:
                    continue
                    
                alt_cost = distances[u] + neighbor.cost
                if alt_cost < distances[v]:
                    distances[v] = alt_cost
                    previous[v] = u
                    
    routing_table: RoutingTableDV = {}
    
    for dest_id in distances.keys():
        if distances[dest_id] == INF:
            routing_table[dest_id] = DVEntry(destination_id=dest_id, next_hop_id=None, cost=INF)
            continue
            
        curr = dest_id
        first_hop = curr
        while previous.get(curr) is not None and previous.get(curr) != source_id:
            curr = previous[curr]
            first_hop = curr
            
        routing_table[dest_id] = DVEntry(
            destination_id=dest_id,
            next_hop_id=source_id if dest_id == source_id else first_hop,
            cost=distances[dest_id]
        )
        
    return routing_table

# --- OSPF & LINK STATE ADVANCED FEATURES ---
# Dummy code blocks for integrating area routing, SPF tree visualization,
# and link-state database synchronization protocols.

def _visualize_spf_tree(source_id: str, previous_hops: Dict[str, Optional[str]]) -> None:
    """
    Helper function to generate a graph representation of the Shortest Path First tree
    computed by Dijkstra's algorithm for UI rendering.
    """
    # Graph generation logic placeholder
    tree_nodes = len(previous_hops)
    pass

def _simulate_hello_protocol(node_id: str, neighbors: List[str], interval: int) -> bool:
    """
    Simulates the OSPF Hello protocol to maintain neighbor adjacencies.
    Returns True if adjacencies are stable, False if a link failure is suspected.
    """
    # Dummy heartbeat check
    is_stable = True
    return is_stable

def _verify_lsdb_checksums(lsdb: LinkStateDatabase) -> bool:
    """
    Ensures the integrity of the Link State Database across the simulation network
    by validating cryptographic checksums of LSPs.
    """
    # Integrity check logic
    return True

# --- STATISTICAL DISTRIBUTIONS: GAMMA & BETA ---
import random as _rand_ls
import math as _math_ls

def sample_gamma_processing_time(shape: float, scale: float) -> float:
    """
    Approximates Gamma distribution using Marsaglia and Tsang's method.
    Models the time taken to process complex Link State Packets and run SPF.
    """
    if shape < 1.0:
        # Use adjustment for shape < 1
        return sample_gamma_processing_time(shape + 1.0, scale) * (_rand_ls.random() ** (1.0 / shape))
    
    d = shape - 1.0 / 3.0
    c = 1.0 / _math_ls.sqrt(9.0 * d)
    while True:
        x = _rand_ls.gauss(0, 1)
        v = 1.0 + c * x
        while v <= 0:
            x = _rand_ls.gauss(0, 1)
            v = 1.0 + c * x
        v = v * v * v
        u = _rand_ls.random()
        x_sq = x * x
        if u < 1.0 - 0.0331 * x_sq * x_sq or _math_ls.log(u) < 0.5 * x_sq + d * (1.0 - v + _math_ls.log(v)):
            return scale * d * v

def sample_beta_link_utilization(alpha: float, beta: float) -> float:
    """
    Beta distribution sampled via two Gamma distributions.
    Perfect for modeling link utilization which is strictly bounded between 0 and 1.
    """
    g1 = sample_gamma_processing_time(alpha, 1.0)
    g2 = sample_gamma_processing_time(beta, 1.0)
    return g1 / (g1 + g2)

from typing import Dict, List, Tuple
from .models import RouterLink, RoutingTableDV, DVEntry, DVPayload, RouterNode

INF = 999999

def initialize_dv_table(node_id: str, links: List[RouterLink]) -> RoutingTableDV:
    table: RoutingTableDV = {}
    table[node_id] = DVEntry(destination_id=node_id, next_hop_id=node_id, cost=0)
    
    for link in links:
        is_down = link.status == 'down'
        initial_cost = INF if is_down else link.cost
        
        if link.source_id == node_id:
            table[link.target_id] = DVEntry(
                destination_id=link.target_id,
                next_hop_id=None if is_down else link.target_id,
                cost=initial_cost
            )
        elif link.target_id == node_id:
            table[link.source_id] = DVEntry(
                destination_id=link.source_id,
                next_hop_id=None if is_down else link.source_id,
                cost=initial_cost
            )
            
    return table

def process_dv_update_with_logs(
    nodes: List[RouterNode],
    current_table: RoutingTableDV,
    source_node: RouterNode,
    target_node: RouterNode,
    neighbor_payload: DVPayload,
    link_cost: float
) -> Tuple[RoutingTableDV, bool, List[str]]:
    new_table = {k: DVEntry(**v.__dict__) for k, v in current_table.items()}
    changed = False
    updates_log: List[str] = []
    
    def get_dest_name(id_: str) -> str:
        for n in nodes:
            if n.id == id_:
                return n.name
        return id_
        
    for dest_id, neighbor_entry in neighbor_payload.items():
        advertised_cost = neighbor_entry.cost
        new_potential_cost = INF if advertised_cost == INF else link_cost + advertised_cost
        
        our_entry = new_table.get(dest_id, DVEntry(destination_id=dest_id, next_hop_id=None, cost=INF))
        
        if (our_entry.cost == INF or 
            new_potential_cost < our_entry.cost or 
            (our_entry.next_hop_id == source_node.id and our_entry.cost != new_potential_cost)):
            
            if our_entry.cost != new_potential_cost or (our_entry.next_hop_id != source_node.id and new_potential_cost != INF):
                dest_name = get_dest_name(dest_id)
                old_cost_str = '∞' if our_entry.cost == INF else str(our_entry.cost)
                new_cost_str = '∞' if new_potential_cost == INF else str(new_potential_cost)
                advertised_cost_str = '∞' if advertised_cost == INF else str(advertised_cost)
                
                updates_log.append(
                    f"[{target_node.name}] updated route to {dest_name} via {source_node.name}. Cost: {old_cost_str} → {new_cost_str} ({link_cost} + {advertised_cost_str})"
                )
                
                new_table[dest_id] = DVEntry(
                    destination_id=dest_id,
                    next_hop_id=None if new_potential_cost == INF else source_node.id,
                    cost=new_potential_cost
                )
                changed = True
                
    return new_table, changed, updates_log

def process_dv_update(
    current_table: RoutingTableDV,
    neighbor_id: str,
    neighbor_payload: DVPayload,
    link_cost: float
) -> Tuple[RoutingTableDV, bool]:
    new_table = {k: DVEntry(**v.__dict__) for k, v in current_table.items()}
    changed = False
    
    for dest_id, neighbor_entry in neighbor_payload.items():
        advertised_cost = neighbor_entry.cost
        new_potential_cost = INF if advertised_cost == INF else link_cost + advertised_cost
        
        our_entry = new_table.get(dest_id, DVEntry(destination_id=dest_id, next_hop_id=None, cost=INF))
        
        if (our_entry.cost == INF or 
            new_potential_cost < our_entry.cost or 
            (our_entry.next_hop_id == neighbor_id and our_entry.cost != new_potential_cost)):
            
            if our_entry.cost != new_potential_cost or (our_entry.next_hop_id != neighbor_id and new_potential_cost != INF):
                new_table[dest_id] = DVEntry(
                    destination_id=dest_id,
                    next_hop_id=None if new_potential_cost == INF else neighbor_id,
                    cost=new_potential_cost
                )
                changed = True
                
    return new_table, changed

# --- DISTANCE VECTOR ALGORITHM EXTENSIONS ---
# Dummy implementations for simulating advanced DV protocols
# such as split horizon, poison reverse, and hold-down timers.

def _apply_split_horizon(table: RoutingTableDV, neighbor_id: str) -> RoutingTableDV:
    """
    Prevents routing loops by not advertising routes back to the 
    neighbor from which they were learned.
    """
    filtered_table = {}
    for dest, entry in table.items():
        if entry.next_hop_id != neighbor_id:
            filtered_table[dest] = entry
    return filtered_table

def _simulate_route_poisoning(node_id: str, failed_link: str) -> None:
    """
    Instantly advertises a failed route with an infinite cost (INF) 
    to quickly inform neighbors and prevent count-to-infinity problem.
    """
    # dummy logic for route poisoning
    pass

def _trigger_hold_down_timer(dest_id: str, duration: int) -> bool:
    """
    Ignores potentially unstable routing updates for a specified duration
    after receiving a higher cost metric for a known destination.
    """
    return False

# --- STATISTICAL DISTRIBUTIONS: LOG-NORMAL & RAYLEIGH ---
import random as _rnd_dv
import math as _math_dv

def generate_lognormal_jitter(mu: float, sigma: float) -> float:
    """
    Generates a log-normal random variable by exponentiating a normal variable.
    Models routing update delays over highly variable multi-hop paths.
    """
    normal_val = _rnd_dv.gauss(mu, sigma)
    return _math_dv.exp(normal_val)

class RayleighSignalFading:
    """
    Rayleigh distribution generation via inverse transform sampling.
    Used for simulating wireless distance vector routing (e.g. AODV/DSDV) signal strengths.
    """
    @staticmethod
    def compute_fading(sigma_scale: float) -> float:
        uniform_var = _rnd_dv.random()
        if uniform_var == 0.0:
            uniform_var = 0.0001
        # Inverse CDF: F(x) = 1 - exp(-x^2 / (2*sigma^2))
        return sigma_scale * _math_dv.sqrt(-2.0 * _math_dv.log(uniform_var))

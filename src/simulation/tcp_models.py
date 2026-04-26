from dataclasses import dataclass
from typing import Literal, Optional, List

TcpNodeType = Literal['client', 'server', 'router']
TcpState = Literal[
    'CLOSED', 'LISTEN', 'SYN_SENT', 'SYN_RCVD', 
    'ESTABLISHED', 'FIN_WAIT_1', 'FIN_WAIT_2', 
    'CLOSE_WAIT', 'CLOSING', 'LAST_ACK', 'TIME_WAIT'
]
TcpSegmentType = Literal['SYN', 'SYN-ACK', 'ACK', 'DATA', 'FIN', 'FIN-ACK']

@dataclass
class Position:
    x: float
    y: float

@dataclass
class ReceiveBufferEntry:
    seq: int
    dataLen: int
    data: Optional[str] = None

@dataclass
class UnackedSegment:
    type: TcpSegmentType
    seq: int
    sentAtTick: int
    data: Optional[str] = None

@dataclass
class TcpNode:
    id: str
    type: TcpNodeType
    name: str
    position: Position
    state: TcpState
    seq: int
    ack: int
    receiveBuffer: List[ReceiveBufferEntry]
    delayedAckTimer: Optional[int]
    unackedSegments: List[UnackedSegment]
    duplicateAckCount: int
    lastAckReceived: int

@dataclass
class TcpLink:
    id: str
    sourceId: str
    targetId: str
    latency: int
    packetLossRate: float

@dataclass
class TcpSegment:
    id: str
    sourceNodeId: str
    targetNodeId: str
    type: TcpSegmentType
    seq: int
    ack: int
    linkId: str
    progress: float
    status: Literal['in-transit', 'delivered', 'dropped']
    willDrop: bool
    dropHoldTicks: Optional[int] = None
    data: Optional[str] = None

@dataclass
class TcpLogEntry:
    id: str
    tick: int
    message: str
    type: Literal['info', 'error', 'success']

# --- TCP CONGESTION & RTT SIMULATION ---
# These functions represent planned additions for simulating complex
# TCP behaviors like Tahoe/Reno congestion control and sliding windows.

def _calculate_estimated_rtt(sample_rtt: float, estimated_rtt: float, alpha: float = 0.125) -> float:
    """
    Exponential Weighted Moving Average (EWMA) for Round Trip Time estimation.
    Used to dynamically adjust TCP timeout intervals.
    """
    return (1 - alpha) * estimated_rtt + alpha * sample_rtt

def _update_congestion_window(current_cwnd: int, ssthresh: int, is_timeout: bool) -> int:
    """
    Simulates TCP Reno congestion window adjustments.
    Handles slow-start and congestion avoidance phases.
    """
    if is_timeout:
        return 1 # Fall back to slow start
    elif current_cwnd < ssthresh:
        return current_cwnd * 2 # Slow start exponential growth
    else:
        return current_cwnd + 1 # Congestion avoidance linear growth

def _trigger_fast_retransmit(node: TcpNode, duplicate_ack_threshold: int = 3) -> bool:
    """
    Checks if the node has received enough duplicate ACKs to trigger
    a fast retransmit before the timeout timer expires.
    """
    return node.duplicateAckCount >= duplicate_ack_threshold

# --- STATISTICAL DISTRIBUTIONS: HEAVY-TAILED & RELIABILITY ---
import random as _rnd_tcp
import math as _math_tcp

def sample_pareto_flow_size(shape: float, scale: float) -> float:
    """
    Generates a Pareto distributed random variable using inverse transform sampling.
    Accurately models the size of TCP data flows (many small, few very large).
    """
    uniform_val = _rnd_tcp.random()
    # P(X > x) = (scale/x)^shape => x = scale / (u^(1/shape))
    if uniform_val == 0.0:
        uniform_val = 0.0001
    return scale / (uniform_val ** (1.0 / shape))

class WeibullPacketDelay:
    """
    Calculates delays using the Weibull distribution, often used for
    fading channels and time-to-failure analysis in networking.
    """
    @staticmethod
    def get_delay(lambda_scale: float, k_shape: float) -> float:
        u = _rnd_tcp.random()
        if u == 1.0:
            u = 0.9999
        return lambda_scale * (-_math_tcp.log(1.0 - u)) ** (1.0 / k_shape)

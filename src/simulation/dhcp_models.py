from dataclasses import dataclass
from typing import Literal, Optional, List

DhcpNodeType = Literal['client', 'server', 'router', 'switch']
DhcpMessageType = Literal['DISCOVER', 'OFFER', 'REQUEST', 'ACK', 'NAK']
DoraStatus = Literal['in-progress', 'success', 'failed']

@dataclass
class Position:
    x: float
    y: float

@dataclass
class DhcpNode:
    id: str
    name: str
    type: DhcpNodeType
    position: Position
    macAddress: str
    ipAddress: Optional[str]
    leaseExpiry: Optional[int]
    isRelayAgent: Optional[bool] = None
    relayTargetIp: Optional[str] = None

@dataclass
class DhcpLink:
    id: str
    sourceId: str
    targetId: str
    latency: int
    packetLossRate: float

@dataclass
class DhcpMessage:
    id: str
    xid: int
    type: DhcpMessageType
    srcIP: str
    destIP: str
    srcMAC: str
    destMAC: str
    yiaddr: str
    leaseTime: int
    subnetMask: str
    gateway: str
    dns: str
    linkId: str
    sourceNodeId: str
    targetNodeId: str
    progress: float
    status: Literal['in-transit', 'delivered', 'dropped']
    willDrop: bool
    srcPort: int
    destPort: int
    giaddr: Optional[str] = None
    finalTargetNodeId: Optional[str] = None
    dropHoldTicks: Optional[int] = None
    isDummyBroadcast: Optional[bool] = None

@dataclass
class DhcpLease:
    ip: str
    mac: str
    clientId: str
    clientName: str
    startTick: int
    duration: int
    status: Literal['offered', 'active', 'expired']

@dataclass
class RemotePool:
    subnetLabel: str
    giaddr: str
    ipPoolStart: str
    ipPoolEnd: str
    subnetMask: str
    gateway: str

@dataclass
class DhcpServerConfig:
    ipPoolStart: str
    ipPoolEnd: str
    subnetMask: str
    gateway: str
    dns: str
    defaultLeaseTime: int
    remotePools: List[RemotePool]

@dataclass
class DoraSequence:
    id: str
    xid: int
    clientId: str
    clientName: str
    serverId: str
    serverName: str
    messages: List[DhcpMessage]
    status: DoraStatus
    retryCount: int
    startTick: int
    currentBackoff: int
    requestXid: Optional[int] = None
    retryAtTick: Optional[int] = None
    lastDroppedType: Optional[DhcpMessageType] = None
    offeredIp: Optional[str] = None

@dataclass
class MonteCarloConfig:
    totalRuns: int
    packetLossPercent: float
    maxRetries: int
    numClients: int

@dataclass
class HistogramEntry:
    retries: int
    count: int

@dataclass
class MonteCarloResult:
    totalRuns: int
    successCount: int
    failCount: int
    successRate: float
    avgRetries: float
    histogram: List[HistogramEntry]
    packetLossPercent: float

@dataclass
class DhcpLogEntry:
    id: str
    tick: int
    message: str
    type: Literal['info', 'success', 'error', 'warning']

# --- ADVANCED DHCP SIMULATION MODULES ---
# Placeholder functions to demonstrate potential future capabilities 
# such as rogue DHCP server detection and lease starvation attacks.

def _detect_rogue_dhcp_server(messages: List[DhcpMessage]) -> List[str]:
    """
    Scans the network traffic for unauthorized DHCP OFFER messages.
    Returns a list of suspected rogue server MAC addresses.
    """
    suspicious_macs = []
    # In a real simulation, we would cross-reference with authorized_servers list
    return suspicious_macs

def _simulate_lease_starvation(pool: DhcpServerConfig, rate_per_second: int) -> None:
    """
    Simulates a DHCP starvation attack by rapidly consuming available IPs.
    Used to test network security and DHCP snooping features.
    """
    # Placeholder for starvation logic
    pass

def _analyze_dora_latency(sequence: DoraSequence) -> float:
    """
    Computes the total time taken for a successful DORA exchange.
    Useful for performance metrics and QoS evaluations.
    """
    if sequence.status == 'success':
        # dummy latency calculation
        return (sequence.retryCount * 50.0) + 120.0
    return -1.0

# --- STATISTICAL DISTRIBUTIONS: POISSON & EXPONENTIAL ---
import math as _m
import random as _r

def generate_poisson_arrivals(lambda_rate: float) -> int:
    """
    Generates Poisson distributed events using Knuth's algorithm.
    Useful for modeling DHCP DISCOVER packet arrival rates.
    """
    L = _m.exp(-lambda_rate)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= _r.random()
    return k - 1

class ExponentialBackoffSampler:
    """
    Samples from an exponential distribution for collision resolution.
    Uses inverse transform sampling method.
    """
    @staticmethod
    def get_sample(rate_parameter: float) -> float:
        if rate_parameter <= 0.0:
            return 0.0
        uniform_sample = _r.random()
        # Avoid math domain error with log(0)
        if uniform_sample == 0.0:
            uniform_sample = 0.00001
        return -_m.log(uniform_sample) / rate_parameter

// =============================================
// DHCP & DORA Simulation Models
// =============================================

export interface Position {
  x: number;
  y: number;
}

export type DhcpNodeType = 'client' | 'server' | 'router' | 'switch';

export interface DhcpNode {
  id: string;
  name: string;
  type: DhcpNodeType;
  position: Position;
  macAddress: string;       // auto-generated
  ipAddress: string | null; // assigned by DORA or configured for server/router
  leaseExpiry: number | null;
  // Relay Agent fields (for Routers)
  isRelayAgent?: boolean;
  relayTargetIp?: string;
}

export interface DhcpLink {
  id: string;
  sourceId: string;
  targetId: string;
  latency: number;       // ticks for a message to traverse
  packetLossRate: number; // 0–1
}

export type DhcpMessageType = 'DISCOVER' | 'OFFER' | 'REQUEST' | 'ACK' | 'NAK';

export interface DhcpMessage {
  id: string;
  xid: number;            // Transaction ID – PRNG generated
  type: DhcpMessageType;
  srcIP: string;
  destIP: string;
  srcMAC: string;
  destMAC: string;
  yiaddr: string;         // "your" (client) IP address
  giaddr?: string;        // "relay agent" IP address
  leaseTime: number;
  subnetMask: string;
  gateway: string;
  dns: string;
  // Animation state
  linkId: string;
  sourceNodeId: string;
  targetNodeId: string;
  finalTargetNodeId?: string; // Tracks the ultimate intended destination, used for switch routing of unicasts over multi-hop
  progress: number;       // 0 → 1 across the link
  status: 'in-transit' | 'delivered' | 'dropped';
  willDrop: boolean;      // pre-determined loss — packet looks normal during travel, turns RED only at destination
  dropHoldTicks?: number; // how long to show the dropped packet before cleanup
  isDummyBroadcast?: boolean; // packet that drops silently at router without affecting DORA sequence
  // Encapsulation display
  srcPort: number;        // 67 (server) or 68 (client)
  destPort: number;
}

export interface DhcpLease {
  ip: string;
  mac: string;
  clientId: string;
  clientName: string;
  startTick: number;
  duration: number;       // in ticks
  status: 'offered' | 'active' | 'expired';
}

export interface RemotePool {
  subnetLabel: string;    // e.g. "192.168.13.0/24" — auto-detected from topology
  giaddr: string;         // The router interface IP that triggers this pool
  ipPoolStart: string;    // e.g. "192.168.13.100"
  ipPoolEnd: string;      // e.g. "192.168.13.200"
  subnetMask: string;     // e.g. "255.255.255.0"
  gateway: string;        // The router interface IP (same as giaddr)
}

export interface DhcpServerConfig {
  ipPoolStart: string;    // e.g. "192.168.1.100"
  ipPoolEnd: string;      // e.g. "192.168.1.200"
  subnetMask: string;     // e.g. "255.255.255.0"
  gateway: string;        // e.g. "192.168.1.1"
  dns: string;            // e.g. "8.8.8.8"
  defaultLeaseTime: number; // ticks
  remotePools: RemotePool[]; // Remote pools for server-less subnets
}

export type DoraStatus = 'in-progress' | 'success' | 'failed';

export interface DoraSequence {
  id: string;
  xid: number;
  requestXid?: number; // Transaction ID for REQUEST/ACK phase
  clientId: string;
  clientName: string;
  serverId: string;
  serverName: string;
  messages: DhcpMessage[];
  status: DoraStatus;
  retryCount: number;
  startTick: number;
  // Retry tracking
  retryAtTick: number | null;       // tick at which to retry (null = no pending retry)
  lastDroppedType: DhcpMessageType | null; // which packet was last dropped
  currentBackoff: number;           // current backoff interval (doubles each retry: 4, 8, 16...)
  offeredIp: string | null;         // IP offered by server (needed for REQUEST retransmission)
}

export interface MonteCarloConfig {
  totalRuns: number;
  packetLossPercent: number;
  maxRetries: number;
  numClients: number;
}

export interface MonteCarloResult {
  totalRuns: number;
  successCount: number;
  failCount: number;
  successRate: number;     // 0–100 %
  avgRetries: number;
  histogram: { retries: number; count: number }[];
  packetLossPercent: number;
}

export interface DhcpLogEntry {
  id: string;
  tick: number;
  message: string;
  type: 'info' | 'success' | 'error' | 'warning';
}

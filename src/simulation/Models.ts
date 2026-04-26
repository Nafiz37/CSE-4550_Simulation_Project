export interface Position {
  x: number;
  y: number;
}

export interface RouterNode {
  id: string;
  name: string;
  position: Position;
  type?: 'router' | 'switch' | 'device';
  // Specific internal states could be added later for visual indicators (e.g. isProcessing, error)
}

export interface RouterLink {
  id: string;
  sourceId: string;
  targetId: string;
  cost: number;
  status?: 'up' | 'down';
  downTicks?: number;
  // Additional properties for advanced simulation (e.g., bandwidth, loss probability)
}

// ---- Distance Vector Models ----
export interface DVEntry {
  destinationId: string;
  nextHopId: string | null;
  cost: number;
}
export type RoutingTableDV = Record<string, DVEntry>; // keyed by destinationId

export interface DVPayloadEntry {
  destinationId: string;
  cost: number;
}
export type DVPayload = Record<string, DVPayloadEntry>;

// ---- Link State Models ----
export interface LSP {
  sourceId: string;
  sequenceNumber: number;
  links: { targetId: string; cost: number }[];
}
export type LinkStateDatabase = Record<string, LSP>; // keyed by sourceId

// ---- Simulation Messaging Models ----
export interface RouteMessage {
  id: string; // unique msg id
  sourceNodeId: string;
  targetNodeId: string;
  linkId: string;
  type: 'LSP_FLOOD' | 'DV_UPDATE';
  payload: any; // RoutingTableDV or LSP
  status?: 'delivered' | 'dropped';
}

export type TcpNodeType = 'client' | 'server' | 'router';

export type TcpState = 
    | 'CLOSED' | 'LISTEN' | 'SYN_SENT' | 'SYN_RCVD' 
    | 'ESTABLISHED' | 'FIN_WAIT_1' | 'FIN_WAIT_2' 
    | 'CLOSE_WAIT' | 'CLOSING' | 'LAST_ACK' | 'TIME_WAIT';

export interface TcpNode {
    id: string;
    type: TcpNodeType;
    name: string;
    position: { x: number; y: number };
    state: TcpState;
    seq: number;
    ack: number;
    receiveBuffer: { seq: number; dataLen: number; data?: string }[];
    delayedAckTimer: number | null;
    unackedSegments: { type: TcpSegmentType, seq: number, data?: string, sentAtTick: number }[];
    duplicateAckCount: number;
    lastAckReceived: number;
}

export interface TcpLink {
    id: string;
    sourceId: string;
    targetId: string;
    latency: number;
    packetLossRate: number;
}

export type TcpSegmentType = 'SYN' | 'SYN-ACK' | 'ACK' | 'DATA' | 'FIN' | 'FIN-ACK';

export interface TcpSegment {
    id: string;
    sourceNodeId: string;
    targetNodeId: string;
    type: TcpSegmentType;
    seq: number;
    ack: number;
    data?: string;
    linkId: string;
    progress: number;
    status: 'in-transit' | 'delivered' | 'dropped';
    willDrop: boolean;
    dropHoldTicks?: number;
}

export interface TcpLogEntry {
    id: string;
    tick: number;
    message: string;
    type: 'info' | 'error' | 'success';
}

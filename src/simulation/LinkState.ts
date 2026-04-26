import type { LSP, LinkStateDatabase, RouterLink, RoutingTableDV } from './Models';

// Reusing INF and DVEntry structure for the final routing table since DV and LS use similar outcome formats
import { INF } from './DistanceVector';

export function generateLSP(nodeId: string, seqNum: number, links: RouterLink[]): LSP {
    const localLinks = links
        .filter((l) => (l.sourceId === nodeId || l.targetId === nodeId) && Math.abs(l.cost) !== Infinity && l.status !== 'down')
        .map((l) => ({
            targetId: l.sourceId === nodeId ? l.targetId : l.sourceId,
            cost: l.cost,
        }));

    return {
        sourceId: nodeId,
        sequenceNumber: seqNum,
        links: localLinks,
    };
}

/**
 * Computes shortest paths using Dijkstra's algorithm based on a full LSDB.
 */
export function calculateDijkstra(sourceId: string, lsdb: LinkStateDatabase): RoutingTableDV {
    const distances: Record<string, number> = {};
    const previous: Record<string, string | null> = {};
    const unvisited = new Set<string>();

    // Initialize
    for (const nodeId of Object.keys(lsdb)) {
        distances[nodeId] = (nodeId === sourceId) ? 0 : INF;
        previous[nodeId] = null;
        unvisited.add(nodeId);
    }

    // Edge case: Add source if it somehow isn't in LSDB
    if (distances[sourceId] === undefined) {
        distances[sourceId] = 0;
        unvisited.add(sourceId);
    }

    while (unvisited.size > 0) {
        // Find node with min distance
        let currentMin = INF;
        let u: string | null = null;

        for (const node of unvisited) {
            if (distances[node] < currentMin) {
                currentMin = distances[node];
                u = node;
            }
        }

        if (u === null || distances[u] === INF) {
            break; // Remaining nodes are unreachable
        }

        unvisited.delete(u);

        // Get neighbors of u from LSDB
        const uLSP = lsdb[u];
        if (uLSP) {
            for (const neighbor of uLSP.links) {
                const v = neighbor.targetId;
                if (!unvisited.has(v)) continue;

                const altCost = distances[u] + neighbor.cost;
                if (altCost < distances[v]) {
                    distances[v] = altCost;
                    previous[v] = u;
                }
            }
        }
    }

    // Construct routing table (resolving the immediate next-hop for each destination)
    const routingTable: RoutingTableDV = {};

    for (const destId of Object.keys(distances)) {
        if (distances[destId] === INF) {
            routingTable[destId] = { destinationId: destId, nextHopId: null, cost: INF };
            continue;
        }

        // Traverse previous map backward to find the first hop
        let curr = destId;
        let firstHop = curr;
        while (previous[curr] !== null && previous[curr] !== sourceId) {
            curr = previous[curr] as string;
            firstHop = curr;
        }

        // If it's the source node itself, the next hop is itself
        routingTable[destId] = {
            destinationId: destId,
            nextHopId: destId === sourceId ? sourceId : firstHop,
            cost: distances[destId],
        };
    }

    return routingTable;
}

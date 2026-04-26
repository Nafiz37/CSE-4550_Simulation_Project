import type { RouterLink, RoutingTableDV } from './Models';

// Infinity in our network simulation
export const INF = 999999;

export function initializeDVTable(nodeId: string, links: RouterLink[]): RoutingTableDV {
    const table: RoutingTableDV = {};

    // Distance to self is 0
    table[nodeId] = { destinationId: nodeId, nextHopId: nodeId, cost: 0 };

    // Initial distances to immediate neighbors
    for (const link of links) {
        const isDown = link.status === 'down';
        const initialCost = isDown ? INF : link.cost;

        if (link.sourceId === nodeId) {
            table[link.targetId] = { destinationId: link.targetId, nextHopId: isDown ? null : link.targetId, cost: initialCost };
        } else if (link.targetId === nodeId) {
            table[link.sourceId] = { destinationId: link.sourceId, nextHopId: isDown ? null : link.sourceId, cost: initialCost };
        }
    }

    return table;
}

export function processDVUpdateWithLogs(
    nodes: import('./Models').RouterNode[],
    currentTable: RoutingTableDV,
    sourceNode: import('./Models').RouterNode,
    targetNode: import('./Models').RouterNode,
    neighborPayload: import('./Models').DVPayload,
    linkCost: number
): { newTable: RoutingTableDV; changed: boolean; updatesLog: string[] } {
    const newTable = { ...currentTable };
    let changed = false;
    const updatesLog: string[] = [];

    const getDestName = (id: string) => nodes.find(n => n.id === id)?.name || id;

    for (const destId of Object.keys(neighborPayload)) {
        const neighborEntry = neighborPayload[destId];
        const advertisedCost = neighborEntry.cost;
        const newPotentialCost = advertisedCost === INF ? INF : linkCost + advertisedCost;
        const ourEntry = newTable[destId] || { destinationId: destId, nextHopId: null, cost: INF };

        if (
            ourEntry.cost === INF ||
            newPotentialCost < ourEntry.cost ||
            (ourEntry.nextHopId === sourceNode.id && ourEntry.cost !== newPotentialCost)
        ) {
            if (ourEntry.cost !== newPotentialCost || (ourEntry.nextHopId !== sourceNode.id && newPotentialCost !== INF)) {

                // Formulate the log message
                const destName = getDestName(destId);
                const oldCostStr = ourEntry.cost === INF ? '∞' : ourEntry.cost.toString();
                const newCostStr = newPotentialCost === INF ? '∞' : newPotentialCost.toString();

                updatesLog.push(
                    `[${targetNode.name}] updated route to ${destName} via ${sourceNode.name}. Cost: ${oldCostStr} → ${newCostStr} (${linkCost} + ${advertisedCost === INF ? '∞' : advertisedCost})`
                );

                newTable[destId] = {
                    destinationId: destId,
                    nextHopId: newPotentialCost === INF ? null : sourceNode.id,
                    cost: newPotentialCost,
                };
                changed = true;
            }
        }
    }

    return { newTable, changed, updatesLog };
}

/**
 * Applies Bellman-Ford algorithm for one iteration based on a received routing table from a neighbor.
 * This simulates a router receiving a DV update from an adjacent router.
 * 
 * @param currentTable The current DV table of our router.
 * @param neighborId The ID of the neighbor sending this payload.
 * @param neighborPayload The distance vector payload from the neighbor (Dest & Cost only).
 * @param linkCost The direct cost of reaching the neighbor from nodeId.
 * @returns An object containing the new table and a boolean `changed` to indicate if triggered updates are needed.
 */
export function processDVUpdate(
    currentTable: RoutingTableDV,
    neighborId: string,
    neighborPayload: import('./Models').DVPayload,
    linkCost: number
): { newTable: RoutingTableDV; changed: boolean } {
    const newTable = { ...currentTable };
    let changed = false;

    for (const destId of Object.keys(neighborPayload)) {
        const neighborEntry = neighborPayload[destId];

        // Standard Distance Vector: neighbor says they can reach destId with cost neighborEntry.cost.
        const advertisedCost = neighborEntry.cost;

        const newPotentialCost = advertisedCost === INF ? INF : linkCost + advertisedCost;

        const ourEntry = newTable[destId] || { destinationId: destId, nextHopId: null, cost: INF };

        // Update if we don't know the route, or the new route is strictly better,
        // OR if this route is currently passing through the neighbor that sent us the update
        // (if the route through our current nextHop got worse, we MUST update our cost to match it).
        if (
            ourEntry.cost === INF ||
            newPotentialCost < ourEntry.cost ||
            (ourEntry.nextHopId === neighborId && ourEntry.cost !== newPotentialCost)
        ) {
            // Wait: only update if it actually changes. A minor edge case is if both are INF.
            if (ourEntry.cost !== newPotentialCost || (ourEntry.nextHopId !== neighborId && newPotentialCost !== INF)) {
                newTable[destId] = {
                    destinationId: destId,
                    nextHopId: newPotentialCost === INF ? null : neighborId,
                    cost: newPotentialCost,
                };
                changed = true;
            }
        }
    }

    return { newTable, changed };
}

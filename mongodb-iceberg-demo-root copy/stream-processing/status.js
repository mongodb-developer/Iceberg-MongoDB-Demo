// Run from mongosh connected to the Stream Processing workspace.
sp.ordersToIceberg.stats({ options: { scale: 1024, verbose: true } });

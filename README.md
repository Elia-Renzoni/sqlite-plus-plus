# sqlite++
Yet another distributed SQLite version

## Overview
SQLite++ is an enhanced, distributed version of SQLite built in Python for both educational purposes and practical applications. This project extends the classic SQLite database with distributed systems capabilities while maintaining the simplicity and ease-of-use that made SQLite popular.

### Features
* Distributed Architecture: Scale beyond single-node limitations
* SQLite Compatibility: Maintains compatibility with standard SQLite syntax and operations
* Python Implementation: Built with modern Python for extensibility and ease of development
* ACID Compliance: Maintains transactional integrity across distributed nodes
* Automatic Failover: Built-in high availability mechanisms

### Architecture
* SQLite++ operates on a cluster of nodes where each node can:
* Serve read/write operations
* Participate in consensus protocols
* Handle distributed transactions
* Detect failures and recover automatically

### Core Components
* Distributed SQL Engine: Parses and routes SQL queries across the cluster
* Consensus Module: Manages node coordination and data consistency
* Transaction Manager: Handles distributed ACID transactions
* Replication Layer: Ensures data redundancy across nodes

## TODO
- [x] API
- [x] Cluster Manager
- [ ] Leader Election
- [x] Failure Detection
- [ ] Distributed Transactions

## How to Run

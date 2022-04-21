# bloxseer

_Chain-data DLC Oracle-as-a-Service API Server_

## Overview

Bloxseer is an oracle management server for discreet log contract (DLC)
events derived from Bitcoin blockchain data. It runs behind an
[Aperture](https://github.com/lightninglabs/aperture) reverse proxy that
facilitates authentication and collection of [Lightning
Network](http://lightning.network/) payments using
[LSATs](https://lsat.tech).

The API server is written in Python using the
[Flask](https://flask.palletsprojects.com/) framwork. The Pricer gRPC
server will be written in Go (using static pricing to start). LSAT data
is stored in [etcd](https://etcd.io/), and DLC data will be stored in
[SQLite](https://sqlite.org/).

DLC operations and blockchain data gathering are managed by
[bitcoin-s](https://bitcoin-s.org/). Pollling is being used initially,
but eventually its `blockprocess` callback will be used to trigger new
block handling. For interfacing with the Lightning Network,
[LND](https://github.com/lightningnetwork/lnd) is used with a
[Neutrino](https://github.com/lightninglabs/neutrino) backend.

High-level architecture diagram:
![Software architecture diagram](docs/overview.png)


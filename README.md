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
[Neutrino](https://github.com/lightninglabs/neutrino) backend (external
LND required at this time).

High-level architecture:
![Software architecture diagram](docs/overview.png)

---

## Usage

### Dev environment

[Polar](https://lightningpolar.com) is recommended for a quick and easy
way to manage a dev environment of regtest LND and bitcoind nodes. For a
detailed walkthrough, visit the [Builder's
Guide](https://docs.lightning.engineering/lapps/guides/polar-lapps/local-cluster-setup-with-polar)

Create a new simnet with 2 LND nodes and 1 bitcoind backend:
- `alice` is used by Aperture
- `bob` is used by the browser

Mine 100 blocks and fund both wallets, then open a channel from `bob`
to `alice`. Copy the macaroons and TLS cert from `alice` into the
`aperture/lnd` directory in this repo:

```
ALICE_LND_DIR="$HOME/.polar/networks/1/volumes/lnd/alice"
ALICE_MACAROON_DIR="$ALICE_LND_DIR/data/chain/bitcoin/regtest"
ALICE_TLS_CERT="$ALICE_LND_DIR/tls.cert"

cp "$ALICE_MACAROON_DIR"/{admin,invoice}".macaroon" $ALICE_TLS_CERT \
  aperture/lnd/
```

In `aperture/aperture.yaml` ensure that `authenticator.lndhost` is set
to the hostname and port where `alice` LND node is listening for gRPC.

Start the bloxseer stack with docker-compose:

```
docker-compose up
```

Now you can try the following endpoints:
- Homepage (Aperture static files): https://localhost:8080
- Events List: https://localhost:8080/event
- New Event: https://localhost:8080/new
  - Requires payment
- Price demo: https://localhost:8080/price
  - Allows 3 free requests, then requires payment

For a walkthrough of how to pay an LSAT invoice, and a deeper dive into
Aperture, watch Elle Mouton's [Aperture Dynamic Prices
Demo](https://www.youtube.com/watch?v=Y2ZG-qcw7Sw). You may also want to
try the [Alby](https://getalby.com/) browser extension.

Wait for the bitcoin-s neutrino client to sync the testnet chain.

Test `bitcoin-s`:

```
curl -v -i -u bitcoins:topsecret --data-binary \
  '{"jsonrpc": "1.0", "id": "curltest", "method": "getinfo", "params":[]}' \
  -H "Content-Type: application/json" http://127.0.0.1:9999/
```

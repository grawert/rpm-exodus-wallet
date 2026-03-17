# Exodus RPM Packaging

Automated RPM packaging workflow for Exodus cryptocurrency wallet.

## Version update

*.envrc*:

```bash
export EXODUS_VERSION=26.3.11
```

## Update spec file

```bash
make version_update
```

## Manual build

### Download

```bash
make download
```

### Build

```bash
make build
```

# futterfabrik

News feed generator for (mostly) german websites

* ARD Mediathek
* ebay Kleinanzeigen
* getnext.to
* picuki (instagram)
* SRF.CH Audio

See also: [RSS Bridge](https://github.com/RSS-Bridge/rss-bridge)

## Deployment

via Docker Compose / Swarm

```yaml
version: '3.9'

services:
  futterfabrik:
    image: ghcr.io/knrdl/futterfabrik
    hostname: futterfabrik
    environment:
      BASE_URL: https://example.org # used for feed urls generation
    ports:
      - "80:80"
    deploy:
      replicas: 1
      update_config:
        order: start-first
      resources:
        reservations:
          memory: 40m
        limits:
          memory: 200m
```

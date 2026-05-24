---
title: Geocoding SN
description: Outil de géocodage en masse d'adresses sénégalaises avec geopy et RateLimiter.
image: ""
tags:
  - Python
  - GeoPandas
  - geopy
category: python
status: en cours
date: "2025-03-20"
link: https://gitlab.com/darcman0
---

# Geocoding SN

Outil de géocodage en masse d'adresses sénégalaises avec geopy et RateLimiter. Optimisé pour les adresses non standardisées en Afrique de l'Ouest.

## Contexte

Le géocodage d'adresses sénégalaises est complexe — les adresses sont souvent non standardisées, incomplètes ou en wolof. Cet outil permet de convertir des milliers d'adresses en coordonnées géographiques de manière automatisée et fiable.

## Fonctionnalités

- Géocodage en masse via l'API Nominatim
- Gestion du rate limiting pour éviter les blocages
- Export en GeoJSON et CSV
- Gestion des erreurs et des adresses non trouvées

## Installation

```bash
pip install geopy geopandas pandas
```

## Utilisation

```python
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

geolocator = Nominatim(user_agent="geocoding-sn")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df = pd.read_csv("adresses.csv")
df["location"] = df["adresse"].apply(geocode)
df["latitude"] = df["location"].apply(lambda x: x.latitude if x else None)
df["longitude"] = df["location"].apply(lambda x: x.longitude if x else None)
```

---

[Voir le dépôt GitLab :fontawesome-brands-gitlab:](https://gitlab.com/darcman0){ .md-button .md-button--primary }
---
date: 
  created: 2025-04-10
authors:
  - darc
categories:
  - Terrain

description: Retour d'expérience sur la cartographie de 2000 hectares de reboisements de mangrove pour WeForest dans le Sine-Saloum et la Casamance. Field report on mapping 2000 hectares of mangrove reforestation for WeForest in Sine-Saloum and Casamance.
---

# Cartographier 2 000 ha de mangroves pour WeForest : retour de terrain
*Mapping 2,000 ha of Mangroves for WeForest: A Field Report*

Entre juillet 2025 et janvier 2026, j'ai participé à la cartographie aérienne de 2 000 hectares de reboisements de mangrove dans les îles du Sine-Saloum et en Casamance pour le compte de WeForest, via Earth Géomatique. 300 sites, plusieurs types de drones, des conditions de terrain extrêmes. Voici ce que j'en retiens.

*Between July 2025 and January 2026, I participated in the aerial mapping of 2,000 hectares of mangrove reforestation in the Sine-Saloum islands and Casamance for WeForest, via Earth Géomatique. 300 sites, multiple drone types, extreme field conditions. Here's what I learned.*

<!-- more -->

---

## Le projet en chiffres · The project in numbers

| | |
|---|---|
| Surface totale | 2 000 ha |
| Nombre de sites | 300 |
| Résolution orthophoto | 2 cm |
| Drones utilisés | DJI Air 2s, Mavic 3 Entreprise, Mavic 3 Mini Pro |
| Outil de suivi terrain | QField |
| Logiciel de traitement | Agisoft Metashape Professional |
| Gain de temps traitement | −20% grâce à l'automatisation |

---

## Les défis du terrain · Field challenges

### Accessibilité des sites · Site accessibility

Le Sine-Saloum est un archipel de bolongs, de chenaux et de mangroves denses. Certains sites ne sont accessibles qu'en pirogue, avec du matériel drone à protéger de l'humidité et des éclaboussures.

*Sine-Saloum is an archipelago of channels and dense mangroves. Some sites are only accessible by dugout canoe, with drone equipment to protect from humidity and splashes.*

**Solution :** Housses étanches pour les batteries et les télécommandes. Vols planifiés au plus tôt le matin pour éviter les vents de mer de l'après-midi.

*Waterproof cases for batteries and controllers. Flights planned early in the morning to avoid afternoon sea winds.*

### Couverture nuageuse · Cloud cover

En saison des pluies, la couverture nuageuse peut invalider des orthophotos entières — les ombres créent des discontinuités radiométriques inutilisables pour la détection de changement.

*During rainy season, cloud cover can invalidate entire orthophotos — shadows create radiometric discontinuities unusable for change detection.*

**Solution :** Planification des vols par fenêtres météo (application Windy + observation locale). Re-vol systématique des zones affectées le jour suivant.

*Flight planning by weather windows (Windy app + local observation). Systematic re-flight of affected zones the next day.*

### Autonomie batterie sur zones étendues · Battery life over large areas

Un site de 10–15 ha nécessite 2 à 3 batteries consécutives. La gestion des rotations de batteries en terrain isolé, sans accès à l'électricité, est un défi logistique réel.

*A 10–15 ha site requires 2 to 3 consecutive batteries. Managing battery rotation in isolated terrain, without electricity access, is a real logistical challenge.*

**Solution :** Panneau solaire portable 100W + banque d'énergie 40 000 mAh pour recharge partielle en journée. Chargeur voiture branché sur le moteur de la pirogue.

*100W portable solar panel + 40,000 mAh power bank for partial daytime recharging. Car charger connected to the dugout canoe engine.*

---

## L'organisation des 300 sites avec QField · Managing 300 sites with QField

QField a été central dans la gestion de la mission. Voici notre workflow :

*QField was central to mission management. Here's our workflow:*

1. **Préparation dans QGIS** : création d'une couche de points pour les 300 sites, avec attributs (ID site, surface estimée, statut, date prévue, commentaires)
2. **Synchronisation sur QField** : chaque télépilote avait sa zone de sites assignée sur sa tablette
3. **Sur le terrain** : remplissage du statut (volé / à re-voler / problème technique), ajout de photos géolocalisées
4. **Synchronisation en fin de journée** : mise à jour de la base centrale via QFieldCloud

*QGIS preparation: creation of a point layer for 300 sites with attributes (site ID, estimated area, status, planned date, comments). QField sync: each pilot had their assigned site zone on their tablet. In the field: status updates (flown / to re-fly / technical issue), addition of geolocated photos. End-of-day sync: update of the central database via QFieldCloud.*

---

## Le traitement dans Metashape · Processing in Metashape

Pour gagner du temps sur 300 lots d'images, j'ai mis en place un workflow semi-automatisé avec les scripts Python de Metashape :

*To save time across 300 image batches, I set up a semi-automated workflow using Metashape's Python scripts:*

```python
import Metashape
import os

doc = Metashape.app.document
chunk = doc.chunk

# Alignement des photos avec paramètres optimisés pour mangrove
chunk.matchPhotos(
    accuracy=Metashape.HighAccuracy,
    generic_preselection=True,
    reference_preselection=True
)
chunk.alignCameras()

# Nuage de points dense
chunk.buildDepthMaps(quality=Metashape.MediumQuality)
chunk.buildDenseCloud()

# Orthophoto 2 cm
chunk.buildOrthomosaic(
    surface=Metashape.ElevationData,
    resolution=0.02  # 2 cm
)

# Export automatique
output_path = "D:/WeForest/outputs/"
chunk.exportOrthomosaic(
    output_path + chunk.label + "_ortho.tif",
    image_format=Metashape.ImageFormatTIFF,
    resolution=0.02
)

print(f"Traitement terminé : {chunk.label}")
```

Ce script, appliqué via le batch processing de Metashape sur des dossiers organisés par site, a réduit le temps de traitement moyen de **20%** en éliminant les étapes manuelles répétitives.

*Applied via Metashape's batch processing on site-organized folders, this script reduced average processing time by **20%** by eliminating repetitive manual steps.*

---

## Ce que j'ai appris · What I learned

!!! success "Ce qui a bien fonctionné · What worked well"
    - QField pour le suivi en temps réel des 300 sites : indispensable
    - Les vols tôt le matin (6h–9h) : lumière rasante, vent faible, mangroves encore humides donc contraste maximal
    - Recouvrement frontal/latéral à 80%/70% : moins de trous dans les zones denses

!!! warning "Ce que je referais différemment · What I'd do differently"
    - Prévoir des GCP même sur des zones plates : la précision verticale s'en ressent
    - Documenter les sites problématiques dès le terrain plutôt qu'en post-traitement
    - Utiliser systématiquement le Mavic 3 Entreprise (RTK intégré) plutôt que l'Air 2s pour les zones critiques

---

*Mission réalisée avec Earth Géomatique pour WeForest, Sénégal, 2025.*  
*Mission carried out with Earth Géomatique for WeForest, Senegal, 2025.*

---
date: 
    created: 2023-05-01
authors:
  - darc
categories:
  - Tutoriels

description: Comment automatiser la génération de 78 PDF de cartes pédologiques avec PyQGIS en utilisant aggregate() et @layout_page. How to automate the generation of 78 pedological map PDFs using PyQGIS with aggregate() and @layout_page.
---

# Automatiser l'export PDF de 78 cartes avec PyQGIS
*Automating the Export of 78 Maps to PDF with PyQGIS*

Dans le cadre d'un projet de cartographie pédologique couvrant 78 parcelles sur 3 régions du Sénégal, j'avais besoin de générer 78 PDF de cartes individuelles automatiquement depuis QGIS. Voici exactement comment j'ai procédé.

*During a pedological mapping project covering 78 parcels across 3 regions of Senegal, I needed to automatically generate 78 individual map PDFs from QGIS. Here's exactly how I did it.*

<!-- more -->

---

## Le contexte · The context

Le projet consistait à cartographier 11 paramètres de fertilité des sols (N, P, K, Ca, Mg, Na, S, MO, CEC, pH, CE) sur 78 parcelles réparties dans 3 régions. Chaque parcelle devait avoir sa propre fiche cartographique en PDF, avec les valeurs du paramètre, la légende et les métadonnées de la parcelle.

Faire ça manuellement = 78 exports × 11 paramètres = **858 opérations**. Inacceptable.

*The project involved mapping 11 soil fertility parameters (N, P, K, Ca, Mg, Na, S, OM, CEC, pH, EC) across 78 parcels in 3 regions. Each parcel needed its own PDF map sheet with parameter values, legend and parcel metadata. Doing this manually = 78 exports × 11 parameters = **858 operations**. Not acceptable.*

---

## La solution : Atlas QGIS + PyQGIS · The solution: QGIS Atlas + PyQGIS

### 1. Configurer l'Atlas dans QGIS · Set up Atlas in QGIS

Dans le gestionnaire de mise en page (Print Layout) :

1. Activer **Atlas** dans le panneau de droite
2. Définir la **couche de couverture** : ta couche de parcelles
3. Cocher **Trier par** : identifiant de parcelle

*In the Print Layout manager:*

1. *Enable **Atlas** in the right panel*
2. *Set the **Coverage layer**: your parcels layer*
3. *Check **Sort by**: parcel identifier*

### 2. Expressions dynamiques dans la mise en page · Dynamic expressions in the layout

Pour afficher automatiquement les valeurs d'une parcelle dans le layout, utilise l'expression `aggregate()` combinée à `@atlas_featureid` :

```
[% aggregate(
    layer := 'parcelles',
    aggregate := 'mean',
    expression := "valeur_n",
    filter := $id = @atlas_featureid
) %]
```

Pour les titres de page dynamiques avec `@layout_page` :

```
[% 'Parcelle N°' || @atlas_featurenumber || ' — Page ' || @layout_page %]
```

### 3. Le script PyQGIS · The PyQGIS script

Une fois l'Atlas configuré dans l'interface, lance l'export en batch depuis la console Python de QGIS :

```python
from qgis.core import QgsProject, QgsPrintLayout, QgsLayoutExporter
import os

# Charger le projet et la mise en page
project = QgsProject.instance()
layout_name = "Fiche_Pedologique"  # nom de ton layout
output_dir = "C:/output/cartes_pdf/"  # dossier de sortie

# Récupérer la mise en page
manager = project.layoutManager()
layout = manager.layoutByName(layout_name)

if layout is None:
    print(f"Layout '{layout_name}' introuvable.")
else:
    atlas = layout.atlas()
    atlas.setEnabled(True)

    # Paramètres d'export PDF
    exporter = QgsLayoutExporter(layout)
    settings = QgsLayoutExporter.PdfExportSettings()
    settings.dpi = 300
    settings.forceVectorOutput = False

    os.makedirs(output_dir, exist_ok=True)

    # Boucle sur toutes les entités de l'Atlas
    atlas.beginRender()
    atlas.first()

    while True:
        # Nom du fichier basé sur un attribut de la parcelle
        feature = atlas.currentFeature()
        parcel_id = feature["id_parcelle"]
        filename = os.path.join(output_dir, f"parcelle_{parcel_id}.pdf")

        result = exporter.exportToPdf(filename, settings)

        if result == QgsLayoutExporter.Success:
            print(f"✓ Exporté : {filename}")
        else:
            print(f"✗ Erreur pour la parcelle {parcel_id}")

        if not atlas.next():
            break

    atlas.endRender()
    print("Export terminé.")
```

### 4. Résultat · Result

- **78 PDF générés** en moins de 4 minutes
- Nommage automatique par identifiant de parcelle
- Résolution 300 DPI prête pour impression

*78 PDFs generated in under 4 minutes. Automatic naming by parcel ID. 300 DPI print-ready resolution.*

---

## Points d'attention · Watch out for

!!! warning "Chemins de fichiers · File paths"
    Sur Windows, utilise des slashs `/` ou doubles backslashs `\\` dans les chemins Python. Un seul `\` provoque des erreurs silencieuses.  
    *On Windows, use forward slashes `/` or double backslashes `\\` in Python paths.*

!!! tip "Tester avant de lancer · Test before running"
    Exporte d'abord 2 ou 3 pages manuellement depuis l'interface pour vérifier que le layout est correct avant de lancer le script complet.  
    *Export 2–3 pages manually from the UI first to verify the layout is correct before running the full script.*

---

## Pour aller plus loin · Going further

- Adapter le script pour exporter en **PNG** ou **SVG** : remplace `exportToPdf` par `exportToImage`
- Ajouter un **paramètre de filtre** pour n'exporter que les parcelles d'une région donnée
- Générer un **fichier de log** CSV avec le statut de chaque export

*Adapt the script to export to **PNG** or **SVG**: replace `exportToPdf` with `exportToImage`. Add a **filter parameter** to export only parcels from a given region. Generate a **CSV log file** with each export's status.*

---

*Article rédigé à partir d'un projet réel de cartographie pédologique au Sénégal (2025).*  
*Written from a real pedological mapping project in Senegal (2025).*

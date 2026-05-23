import os
import yaml
import nbformat

def get_md_metadata(filepath):
    """Lit le front matter d'un fichier .md"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            try:
                return yaml.safe_load(content[3:end])
            except:
                return {}
    return {}

def get_ipynb_metadata(filepath):
    """Lit le front matter depuis la première cellule Raw d'un notebook"""
    try:
        nb = nbformat.read(filepath, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == "raw":
                source = cell.source.strip()
                if source.startswith("---"):
                    end = source.find("---", 3)
                    if end != -1:
                        try:
                            return yaml.safe_load(source[3:end])
                        except:
                            return {}
    except:
        return {}
    return {}

def get_items(docs_dir, subfolder):
    """Scanne un dossier et retourne les métadonnées de chaque fichier"""
    folder = os.path.join(docs_dir, subfolder)
    items = []
    if not os.path.exists(folder):
        return items
    for filename in sorted(os.listdir(folder)):
        if filename in ["index.md", ".pages"]:
            continue
        if filename.startswith("_") or filename.startswith("sample"):
            continue
        filepath = os.path.join(folder, filename)
        meta = {}
        if filename.endswith(".md"):
            meta = get_md_metadata(filepath)
            meta["_file"] = filename.replace(".md", "")
            meta["_notebook"] = False
        elif filename.endswith(".ipynb"):
            meta = get_ipynb_metadata(filepath)
            meta["_file"] = filename.replace(".ipynb", "")
            meta["_notebook"] = True
        else:
            continue
        if meta.get("title"):
            items.append(meta)
    items.sort(key=lambda x: str(x.get("date", "") or ""), reverse=True)
    return items

def define_env(env):
    docs_dir = env.conf["docs_dir"]

    @env.macro
    def render_projects():
        items = get_items(docs_dir, "projects")
        return _render_cards(items, "projects")

    @env.macro
    def render_apps():
        items = get_items(docs_dir, os.path.join("app", "apps"))
        return _render_cards(items, "app/apps")

def _render_cards(items, section):
    if not items:
        return "<p><em>Aucun élément pour l'instant.</em></p>"

    cards = []
    for item in items:
        title = item.get("title", "")
        description = item.get("description", "")
        tags = item.get("tags", [])
        status = item.get("status", "")
        image = item.get("image", "") or ""
        notebook = item.get("_notebook", False)
        file_slug = item.get("_file", "")

        # Lien interne vers la page
        href = f"../{section}/{file_slug}/"

        # Badge statut
        status_colors = {
            "terminé": ("#d4edda", "#155724", "✓ Terminé"),
            "en cours": ("#fff3cd", "#856404", "⟳ En cours"),
            "idée": ("#e2e3e5", "#383d41", "✦ Idée"),
        }
        sc = status_colors.get(status.lower(), ("#e2e3e5", "#383d41", status))
        status_badge = f'<span style="font-size:0.75rem;font-weight:600;padding:2px 8px;border-radius:12px;background:{sc[0]};color:{sc[1]}">{sc[2]}</span>' if status else ""

        notebook_badge = '<span style="font-size:0.75rem;font-weight:600;padding:2px 8px;border-radius:12px;background:#e6f1fb;color:#185fa5;margin-left:4px">📓 Notebook</span>' if notebook else ""

        # Image
        img_html = f'<img src="{image}" alt="{title}" style="width:100%;height:160px;object-fit:cover;border-radius:4px;margin-bottom:0.75rem">' if image else '<div style="width:100%;height:100px;background:var(--md-code-bg-color);border-radius:4px;margin-bottom:0.75rem;display:flex;align-items:center;justify-content:center;color:var(--md-default-fg-color--light);font-size:0.8rem">Pas d\'image</div>'

        # Tags
        tags_html = " ".join([f'<code style="font-size:0.75rem">{t}</code>' for t in tags])

        card = f"""<div class="project-card" style="display:flex;flex-direction:column;gap:0.5rem">
{img_html}
<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">{status_badge}{notebook_badge}</div>
<strong>{title}</strong>
<p style="font-size:0.85rem;color:var(--md-default-fg-color--light);margin:0">{description}</p>
<div>{tags_html}</div>
<a href="{href}" class="md-button" style="margin-top:auto;align-self:flex-start">Lire →</a>
</div>"""
        cards.append(card)

    return '<div class="grid">\n' + "\n".join(cards) + "\n</div>"
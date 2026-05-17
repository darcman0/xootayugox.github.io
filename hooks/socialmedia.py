from textwrap import dedent
import urllib.parse

x_intent = "https://x.com/intent/tweet"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
linkedin_sharer = "https://www.linkedin.com/sharing/share-offsite/"

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']
    
    # Applique les boutons uniquement sur les articles de blog
    if page.meta.get('template') != 'blog-post.html': 
        return markdown

    # Sécurisation de la construction de l'URL pour éviter le crash CI/CD
    base_url = config.site_url or "https://xootayugox.github.io"
    page_url = f"{base_url.rstrip('/')}/{page.url}"
    
    page_title = urllib.parse.quote(page.title + '\n')

    # Utilisation de Flexbox pour un alignement dynamique et espacé
    return markdown + dedent(f"""
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #444;" markdown="1">
    <h3 style="text-align: center; font-weight: bold; margin-bottom: 20px;">Partager cet article</h3>
    
    <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;" markdown="1">
    
    [Sur :simple-x:]({x_intent}?text={page_title}&url={page_url}){{ .md-button }}
    [Sur :simple-facebook:]({fb_sharer}?u={page_url}){{ .md-button }}
    [Sur :fontawesome-brands-linkedin:]({linkedin_sharer}?url={page_url}){{ .md-button }}
    
    </div>
    </div>
    """)
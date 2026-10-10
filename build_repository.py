"""Genera sito statico e repository Kodi; solo libreria standard Python."""
import argparse
import hashlib
import html
from pathlib import Path
import shutil
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


def build(base_url, output):
    base_url = base_url.rstrip('/')
    if urlparse(base_url).scheme != 'https' or not urlparse(base_url).netloc:
        raise ValueError('Serve un URL HTTPS pubblico.')
    source = Path(__file__).resolve().parent / 'plugin.video.streamit'
    addon = ET.parse(source / 'addon.xml').getroot()
    output.mkdir(parents=True, exist_ok=True)
    repo = ET.Element('addon', id='repository.streamit', name='StreamIt Repository',
                      version='1.0.5', **{'provider-name': 'StreamIt'})
    requires = ET.SubElement(repo, 'requires')
    ET.SubElement(requires, 'import', addon='xbmc.addon', version='19.0.0')
    extension = ET.SubElement(repo, 'extension', point='xbmc.addon.repository', name='StreamIt')
    directory = ET.SubElement(extension, 'dir', minversion='19.0.0')
    index_url = 'https://raw.githubusercontent.com/BONALAPIZZA9/streamit/main/kodi'
    ET.SubElement(directory, 'info').text = index_url + '/addons-' + repo.get('version') + '.xml'
    ET.SubElement(directory, 'checksum', verify='sha256').text = index_url + '/addons-' + repo.get('version') + '.xml.sha256'
    ET.SubElement(directory, 'datadir').text = base_url + '/'
    meta = ET.SubElement(repo, 'extension', point='xbmc.addon.metadata')
    ET.SubElement(meta, 'summary', lang='it_IT').text = 'Installazione e aggiornamenti di StreamIt'
    ET.SubElement(meta, 'description', lang='it_IT').text = 'Repository personale StreamIt per Kodi 19 e successivi.'
    ET.SubElement(meta, 'platform').text = 'all'
    ET.SubElement(meta, 'license').text = 'GPL-2.0-or-later'
    assets = ET.SubElement(meta, 'assets')
    ET.SubElement(assets, 'icon').text = 'icon.png'
    repo_xml = ET.tostring(repo, encoding='utf-8', xml_declaration=True)
    icon = source / 'resources/media/icon.png'
    repo_dir = output / 'repository.streamit'
    repo_dir.mkdir(exist_ok=True)
    repo_zip = repo_dir / 'repository.streamit-1.0.5.zip'
    with zipfile.ZipFile(repo_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('repository.streamit/', b'')
        archive.writestr('repository.streamit/addon.xml', repo_xml)
        archive.write(icon, 'repository.streamit/icon.png')
    (repo_dir / 'addon.xml').write_bytes(repo_xml)
    shutil.copy2(icon, repo_dir / 'icon.png')
    shutil.copy2(repo_zip, output / repo_zip.name)
    shutil.copy2(repo_zip, output / 'repository.streamit-1.0.0.zip')
    addon_dir = output / addon.get('id')
    addon_dir.mkdir(exist_ok=True)
    addon_zip = addon_dir / (addon.get('id') + '-' + addon.get('version') + '.zip')
    with zipfile.ZipFile(addon_zip, 'w', zipfile.ZIP_STORED) as archive:
        archive.writestr(source.name + '/', b'')
        for path in sorted(source.rglob('*')):
            if '__pycache__' in path.parts or path.suffix == '.pyc':
                continue
            name = path.relative_to(source.parent).as_posix()
            if path.is_dir():
                archive.writestr(name + '/', b'')
            else:
                archive.write(path, name)
    # Kodi legge le immagini dal percorso dichiarato nel manifest.
    for asset in addon.findall('./extension[@point="xbmc.addon.metadata"]/assets/*'):
        if asset.text:
            dest = addon_dir / asset.text
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / asset.text, dest)
    shutil.copy2(source / 'addon.xml', addon_dir / 'addon.xml')
    listing = ET.Element('addons')
    listing.extend([repo, addon])
    xml = ET.tostring(listing, encoding='utf-8', xml_declaration=True)
    (output / 'addons.xml').write_bytes(xml)
    (output / 'addons.xml.sha256').write_text(hashlib.sha256(xml).hexdigest(), encoding='ascii')
    shutil.copy2(output / 'addons.xml', output / ('addons-' + repo.get('version') + '.xml'))
    shutil.copy2(output / 'addons.xml.sha256', output / ('addons-' + repo.get('version') + '.xml.sha256'))
    (output / '.nojekyll').touch()
    link = addon_zip.relative_to(output).as_posix()
    (output / 'index.html').write_text('''<!doctype html><html lang="it"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>StreamIt per Kodi</title>
<style>body{background:#0c1b2f;color:#def3fa;font:18px system-ui;max-width:720px;margin:60px auto;padding:24px}a{color:#23dcda}li{margin:16px 0}img{width:100px;border-radius:24px}</style>
<img src="repository.streamit/icon.png" alt="StreamIt"><h1>StreamIt per Kodi</h1>
<p>Aggiungi questo indirizzo come sorgente in Gestione file di Kodi:</p><p><code>'''
        + html.escape(base_url + '/') + '''</code></p><ul><li><a href="repository.streamit-1.0.5.zip">repository.streamit-1.0.5.zip</a></li>
<li><a href="''' + html.escape(link) + '''">StreamIt — ZIP diretto</a></li></ul>
<p>In Kodi: Installa da file ZIP → scegli la sorgente → repository.streamit-1.0.5.zip.
Poi: Installa da repository → StreamIt Repository → Add-on video → StreamIt.</p></html>''', encoding='utf-8')
    for path in (repo_zip, addon_zip):
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
    print('Repository generato:', output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--output', default='_site', type=Path)
    args = parser.parse_args()
    build(args.base_url, args.output)


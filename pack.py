#!/usr/bin/env python
# Packages the project for releasing to the Chrome web store.
import os
import zipfile
import json

def make_zipfile(output_filename, source_dir):
  relroot = os.path.abspath(source_dir)
  print "Relroot", relroot
  with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
    for root, dirs, files in os.walk(source_dir):
      # add directory (needed for empty dirs)
      zip.write(root, os.path.relpath(root, relroot))
      for file in files:
        filename = os.path.join(root, file)
        if os.path.isfile(filename): # regular files only
          arcname = os.path.join(os.path.relpath(root, relroot), file)
          zip.write(filename, arcname)
          print "Packing", filename, arcname

def increase_version(major, minor, build):
  build += 1
  if build % 100 == 0:
    build = 0
    minor += 1
    if minor % 10 == 0:
      minor = 0
      major += 1
  return [major, minor, build]

def upgrade_version(manifest_path):
  with open(manifest_path, "r") as f:
    manifest = json.load(f)
  parts = [int(part) for part in manifest["version"].split(".")]
  version = increase_version(*parts)
  version = ".".join([str(part) for part in version])
  manifest["version"] = version
  print "Upgraded to version", version
  with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)
  return version

if __name__ == '__main__':
  new_version = upgrade_version("src/manifest.json")
  filename = 'dist/poloniex-ninja-%s.zip' % new_version
  if os.path.exists(filename):
    os.remove(filename)
  make_zipfile(filename, "src")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os

import omero
from omero.cli import cli_login
from omero.gateway import BlitzGateway

BF_CACHE = "/data/OMERO/BioFormatsCache"
MANAGED_REPO = "data/OMERO/ManagedRepository"

def delete_memo_file(plate):
    for well in plate.listChildren():
        for well_sample in well.listChildren():
            imported_paths = well_sample.getImage().getImportedImageFilePaths()
            for import_file in imported_paths['server_paths':
                if import_file.endswith(".wpi"):
                    break
            assert import_file.endswith(".wpi")
            memo_filename = '.' + os.path.basename(import_file) + '.bfmemo'
            memo_filepath = os.path.join(
                BF_CACHE,
                MANAGED_REPO,
                os.path.dirname(import_file),
                memo_filename
            )
            if os.path.exists(memo_filepath):
                logging.info(f"Deleting memo file for {plate.getName()}")
                os.remove(memo_filepath)
            return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--quiet', '-q', action='count', default=0)
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO - 10 * args.verbose + 10 * args.quiet)

    with omero.cli.cli_login() as c:
        conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
        screen = conn.getObject("Screen", attributes={
            'name': 'idr0088-cox-phenomicprofiling/screenA'})
        for plate in screen.listChildren():
            delete_memo_file(plate)

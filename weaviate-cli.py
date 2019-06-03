#!/usr/bin/env python3
##                          _       _
##__      _____  __ ___   ___  __ _| |_ ___
##\ \ /\ / / _ \/ _` \ \ / / |/ _` | __/ _ \
## \ V  V /  __/ (_| |\ V /| | (_| | ||  __/
##  \_/\_/ \___|\__,_| \_/ |_|\__,_|\__\___|
##
## Copyright © 2016 - 2018 Weaviate. All rights reserved.
## LICENSE: https://github.com/creativesoftwarefdn/weaviate/blob/develop/LICENSE.md
## AUTHOR: Bob van Luijt (bob@kub.design)
## See www.creativesoftwarefdn.org for details
## Contact: @CreativeSofwFdn / bob@kub.design
##

"""This is the main module for the Weaviate-cli tool."""
import argparse
import os
from modules.Init import Init
from modules.Weaviate import Weaviate
from modules.Messages import Messages
from modules.Helpers import Helpers

def main():
    """This class reads the command line arguments and loads the correct modules."""

    # Get parsed arguments
    args = argparse.ArgumentParser(description=Messages().Get(112))

    # Get the arguments for sinit
    args.add_argument('--init', help=Messages().Get(100), action="store_true")
    args.add_argument('--init-url', default=None, help=Messages().Get(101))
    args.add_argument('--init-email', default=None, help=Messages().Get(101))
    args.add_argument('--init-auth', default=None, help=Messages().Get(134))
    args.add_argument('--init-auth-url', default=None, help=Messages().Get(139))
    args.add_argument('--init-auth-clientid', default=None, help=Messages().Get(135))
    args.add_argument('--init-auth-granttype', default=None, help=Messages().Get(136))
    args.add_argument('--init-auth-clientsecret', default=None, help=Messages().Get(137))
    args.add_argument('--init-auth-realmid', default=None, help=Messages().Get(138))

    # Get the arguments for schema import
    args.add_argument('--schema-import', help=Messages().Get(104), action="store_true")
    args.add_argument('--schema-import-ontology', default=None, help=Messages().Get(104))
    args.add_argument('--schema-import-overwrite', help=Messages().Get(107), action="store_true")

    # Get the arguments for schema export
    args.add_argument('--schema-export', help=Messages().Get(108), action="store_true")
    args.add_argument('--schema-export-location', default=None, help=Messages().Get(109))

    # truncate the schema
    args.add_argument('--schema-truncate', help=Messages().Get(126), action="store_true")
    args.add_argument('--schema-truncate-force', help=Messages().Get(127), action="store_true")

    # Empty a weaviate
    args.add_argument('--empty', help=Messages().Get(121), action="store_true")
    args.add_argument('--empty-force', help=Messages().Get(122), action="store_true")

    # Ping a Weaviate
    args.add_argument('--ping', help=Messages().Get(140), action="store_true")

    # Show version
    args.add_argument('--version', help=Messages().Get(121), action="store_true")

    options = args.parse_args()

    # Check init and validate if set
    if options.init is True:
        Init().setConfig(options)
    elif options.version is True:
        with open(os.path.dirname(os.path.realpath(__file__))+"/version", "r") as fh:
            print(fh.read())
            exit(0)

    # Set the config
    config = Init().loadConfig()

    # Check which items to load
    if options.schema_import is True:
        from modules.SchemaImport import SchemaImport
        # Ping Weaviate to validate the connection
        Weaviate(config).Ping()
        SchemaImport(config).Run(options.schema_import_ontology, options.schema_import_overwrite)
    elif options.schema_export is True:
        from modules.SchemaExport import SchemaExport
        # Ping Weaviate to validate the connection
        Weaviate(config).Ping()
        SchemaExport(config).Run()
    elif options.empty is True:
        from modules.Empty import Empty
        # Ping Weaviate to validate the connection
        Weaviate(config).Ping()
        Empty(config).Run(options.empty_force)
    elif options.schema_truncate is True:
        from modules.Truncate import Truncate
        # Ping Weaviate to validate the connection
        Weaviate(config).Ping()
        Truncate(config).Run(options.schema_truncate_force)
    elif options.ping is True:
        Weaviate(config).Ping()
    elif options.init is not True:
        Helpers(None).Info("\n" + Messages().Get(133))
        exit(0)
    else:
        exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Helpers(None).Info("\n" + Messages().Get(213))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import falcon
from wsgiref.simple_server import make_server
import json
from dynaconf import Dynaconf

# Configuration
settings = Dynaconf(settings_files=["../config/settings.yaml"])
port = settings.server.port

runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))
from lib.cpeguesser import CPEGuesser
from lib.utils import ManageSearch


class Search:
    def on_post(self, req, resp):
        data_post = req.bounded_stream.read()
        js = data_post.decode("utf-8")
        try:
            q = json.loads(js)
        except ValueError:
            resp.status = falcon.HTTP_400
            resp.media = "Missing query array or incorrect JSON format"
            return
        print("Q:/n",q)
        request_version = q["version"] if "version" in q else "" 
        request_type = q["type"] if "type" in q else "a" 
        request_limit = q["limit"] if "limit" in q else 5 
        if "query" in q:
            pass
        else:
            resp.status = falcon.HTTP_400
            resp.media = "Missing query array or incorrect JSON format"
            return

        cpeGuesser = CPEGuesser()
        sorted_list = cpeGuesser.guessCpe(q["query"],request_type)
        searchManager= ManageSearch()
        best_matching_version=searchManager.search(sorted_list,request_type,q["query"],request_version,request_limit)
        resp.media = best_matching_version


if __name__ == "__main__":
    app = falcon.App()
    app.add_route("/search", Search())

    try:
        with make_server("0.0.0.0", port, app) as httpd:
            print(f"Serving on port {port}...")
            httpd.serve_forever()
    except OSError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)

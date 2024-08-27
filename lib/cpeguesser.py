#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from dynaconf import Dynaconf

# Configuration
settings = Dynaconf(settings_files=["../config/settings.yaml"])


class CPEGuesser:
    def __init__(self):
        self.rdb = redis.Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=8,
            decode_responses=True,
        )

    def guessCpe(self, words, asset_type="a"):
        k = []
        for keyword in words:
            k.append(f"w:{keyword.lower()}")

        # maxinter = len(k)
        # cpes = []
        # Old script that i found useless but we will keep it we never know
        # for x in reversed(range(maxinter)):
        #     ret = self.rdb.sinter(k[x])
        #     cpes.append(list(ret))
        # result = set(cpes[0]).intersection(*cpes)
        result = self.rdb.sinter(k)

        ranked = []
        
        for cpe in result:
            # Filter by asset type
            if f"cpe:2.3:{asset_type}:" in cpe:
                parts = cpe.split(':')
                # Get all available versions for a given type-editor-product  
                versions = self.rdb.smembers(f"w_{asset_type}_v:{cpe}")
                if len(parts) >= 1:
                    # remove the product string from the versions set
                    versions.discard(parts[-1])
                    # Cast the versions to a list an sort it  
                    versions = list(versions)
                    versions.sort()
                #get the index ranking for each given type-editor-product 
                # rank = self.rdb.zrank("rank:cpe", cpe)
                ranked.append((cpe, versions))
        return sorted(ranked)

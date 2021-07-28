#!/usr/bin/env python

"""
Separate models are being trained per (almost) non-overlaping entity groups,
that is groups guaranteeing it is at least highly unlikely entities within
will collide. Whenever possible, groups consisted of neighboring entities
in order to exploit the potential of linear CRF chain.
"""

GROUPS = (['persName'],
          ['orgName'],
          ['geogName', 'placeName'],
          ['placeName_bloc', 'placeName_region', 'placeName_country', 'placeName_district', 'placeName_settlement'],)

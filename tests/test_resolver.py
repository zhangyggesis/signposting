"""Test the resolver"""

import unittest
from unittest.mock import Mock, MagicMock, patch

from signposting.resolver import find_signposting_http
import urllib.error

import os
import warnings

@unittest.skipIf("CI" in os.environ, "Integration tests requires network access")
class TestResolverA2A(unittest.TestCase):

    def test_00_404(self):
        with self.assertRaises(urllib.error.HTTPError):
            find_signposting_http("https://w3id.org/a2a-fair-metrics/00-404-not-found/")

    def test_01_describedby(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/01-http-describedby-only/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/01-http-describedby-only/index.ttl")
        self.assertFalse("type" in s.describedBy[0])

    def test_02_html_only(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/02-html-full/")
        self.assertIsNone(s.citeAs) # only in HTML

    def test_03_citeas(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/03-http-citeas-only/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/03-http-citeas-only/")

    def test_04_iri(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/04-http-describedby-iri/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, 
            "https://xn--11-slc.xn--e1a4c/2022/a2a-fair-metrics/04-http-describedby-iri/index.ttl")
            # e.g. "https://з11.ею/2022/a2a-fair-metrics/04-http-describedby-iri/index.ttl")

    def test_05_describedby_citeas(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/05-http-describedby-citeas/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/05-http-describedby-citeas/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/05-http-describedby-citeas/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")

    def test_06_describedby_citeas_item(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/06-http-citeas-describedby-item/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/06-http-citeas-describedby-item/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/06-http-citeas-describedby-item/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        self.assertEqual(1, len(s.item))
        self.assertEqual(s.item[0].target, "https://s11.no/2022/a2a-fair-metrics/06-http-citeas-describedby-item/test-apple-data.csv")
        self.assertEqual(s.item[0]["type"], "text/csv")    

    def test_07_describedby_citeas_linkset(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/07-http-describedby-citeas-linkset-json/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/07-http-describedby-citeas-linkset-json/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/07-http-describedby-citeas-linkset-json/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        self.assertEqual(1, len(s.linkset))
        self.assertEqual(s.linkset[0].target, "https://s11.no/2022/a2a-fair-metrics/07-http-describedby-citeas-linkset-json/linkset.json")
        self.assertEqual(s.linkset[0]["type"], "application/linkset+json")    

    def test_08_describedby_citeas_linkset_txt(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/08-http-describedby-citeas-linkset-txt/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/08-http-describedby-citeas-linkset-txt/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/08-http-describedby-citeas-linkset-txt/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        self.assertEqual(1, len(s.linkset))
        self.assertEqual(s.linkset[0].target, "https://s11.no/2022/a2a-fair-metrics/08-http-describedby-citeas-linkset-txt/linkset.txt")
        self.assertEqual(s.linkset[0]["type"], "application/linkset")
        # TODO: Check content of linkset

    def test_09_describedby_citeas_linkset_json_txt(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/09-http-describedby-citeas-linkset-json-txt/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/09-http-describedby-citeas-linkset-json-txt/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/09-http-describedby-citeas-linkset-json-txt/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        self.assertEqual(2, len(s.linkset))
        self.assertEqual(s.linkset[0].target, "https://s11.no/2022/a2a-fair-metrics/09-http-describedby-citeas-linkset-json-txt/linkset.json")
        self.assertEqual(s.linkset[0]["type"], "application/linkset+json")    
        self.assertEqual(s.linkset[1].target, "https://s11.no/2022/a2a-fair-metrics/09-http-describedby-citeas-linkset-json-txt/linkset.txt")
        self.assertEqual(s.linkset[1]["type"], "application/linkset")    

    def test_10_describedby_citeas_linkset_txt(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/10-http-citeas-not-perma/")
        self.assertEqual(s.citeAs.target, 
            "https://example.org/a2a-fair-metrics/10-http-citeas-not-perma/")

    def test_11_iri_wrong_type(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/11-http-described-iri-wrong-type/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, 
            "https://xn--11-slc.xn--e1a4c/2022/a2a-fair-metrics/11-http-described-iri-wrong-type/index.ttl")
        self.assertEqual(s.describedBy[0]["type"],
            "text/html") # which is wrong, but correct for this test

    def test_12_item_not_found(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/12-http-item-does-not-resolve/")
        self.assertEqual(1, len(s.item))
        self.assertEqual(s.item[0].target, "https://s11.no/2022/a2a-fair-metrics/12-http-item-does-not-resolve/fake.ttl")
            # .. which is  404 Not Found, but not our job to test
        self.assertFalse("type" in s.item[0])

    def test_13_describedby(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/13-http-describedby-with-type/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/13-http-describedby-with-type/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")

    def test_14_describedby_citeas_linkset_json_txt_conneg(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/14-http-describedby-citeas-linkset-json-txt-conneg/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/14-http-describedby-citeas-linkset-json-txt-conneg/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/14-http-describedby-citeas-linkset-json-txt-conneg/index.ttl")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        # FIXME: Don't assume particular order
        self.assertEqual(2, len(s.linkset))
        self.assertEqual(s.linkset[0].target, "https://s11.no/2022/a2a-fair-metrics/14-http-describedby-citeas-linkset-json-txt-conneg/linkset")
        self.assertEqual(s.linkset[0]["type"], "application/linkset+json")    
        self.assertEqual(s.linkset[1].target, "https://s11.no/2022/a2a-fair-metrics/14-http-describedby-citeas-linkset-json-txt-conneg/linkset")
        self.assertEqual(s.linkset[1]["type"], "application/linkset")

    def test_15_describedby_no_conneg(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/15-http-describedby-no-conneg/")
        # FIXME: Don't assume particular order
        self.assertEqual(2, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/15-http-describedby-no-conneg/metadata.ttl")
        self.assertEqual(s.describedBy[1].target, "https://s11.no/2022/a2a-fair-metrics/15-http-describedby-no-conneg/metadata.jsonld")
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        self.assertEqual(s.describedBy[1]["type"], "application/ld+json")

    def test_16_describedby_nconneg(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/16-http-describedby-conneg/")
        # FIXME: Don't assume particular order
        self.assertEqual(2, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, "https://s11.no/2022/a2a-fair-metrics/16-http-describedby-conneg/metadata")
        self.assertEqual(s.describedBy[1].target, "https://s11.no/2022/a2a-fair-metrics/16-http-describedby-conneg/metadata") # same as above
        self.assertEqual(s.describedBy[0]["type"], "text/turtle")
        self.assertEqual(s.describedBy[1]["type"], "application/ld+json") ## .. e.g. have to content-negotiate

    def test_17_multiple_rels(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/17-http-citeas-multiple-rels/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/17-http-citeas-multiple-rels/")
        self.assertEqual(s.citeAs.rel, 
            # TODO: Do we require the remaining rels to be preserved?
            set(("canonical", "cite-as", "http://schema.org/identifier")))

    def test_18_html_only(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/18-html-citeas-only/")
        self.assertIsNone(s.citeAs) # only in HTML

    def test_19_html_only(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/19-html-citeas-multiple-rels/")
        self.assertIsNone(s.citeAs) # only in HTML

    def test_20_citeas(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/20-http-html-citeas-same/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/20-http-html-citeas-same/")

    def test_21_citeas_differ(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/21-http-html-citeas-differ/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/21-http-html-citeas-differ/")
            # while HTML would give different PID
    def test_22_citeas_mixed(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/22-http-html-citeas-describedby-mixed/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/22-http-html-citeas-describedby-mixed/")
        self.assertEqual([], s.describedBy) # only in HTML            

    def test_23_complete(self):
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/23-http-citeas-describedby-item-license-type-author/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/23-http-citeas-describedby-item-license-type-author/")
        self.assertEqual(1, len(s.describedBy))
        self.assertEqual(s.describedBy[0].target, 
            "https://s11.no/2022/a2a-fair-metrics/23-http-citeas-describedby-item-license-type-author/index.ttl")
        self.assertEqual(s.describedBy[0]["type"],                     
            "text/turtle")
        self.assertEqual(s.item[0].target, 
            "https://s11.no/2022/a2a-fair-metrics/23-http-citeas-describedby-item-license-type-author/test-apple-data.csv")
        self.assertEqual(s.item[0]["type"],                     
            "text/csv")

    def test_24_citeas_no_content(self):
        # This will give 204 No Content and has no content on GET
        # but still contain signposting.
        s = find_signposting_http("https://w3id.org/a2a-fair-metrics/24-citeas-204-no-content/")
        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/24-citeas-204-no-content/")

    def test_25_citeas_gone(self):
        # This will throw 410 Gone but still contain thumbstone headers
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            s = find_signposting_http("https://w3id.org/a2a-fair-metrics/25-citeas-author-410-gone/")
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "410 Gone" in str(w[0].message)

        self.assertEqual(s.citeAs.target, 
            "https://w3id.org/a2a-fair-metrics/25-citeas-author-410-gone/")
        self.assertEqual(1, len(s.author))
        self.assertEqual(s.author[0].target, 
            "https://orcid.org/0000-0002-1825-0097")

    def test_26_citeas_non_authorative(self):
        # This will give 26 Non-Authorative and may be rewritten by a proxy
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            s = find_signposting_http("https://w3id.org/a2a-fair-metrics/26-citeas-203-non-authorative/")
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "203 Non-Authoritative Information" in str(w[0].message)
        self.assertEqual(s.citeAs.target, 
            # Deliberately "rewritten" PID
            "https://example.com/rewritten/w3id.org/a2a-fair-metrics/26-citeas-203-non-authorative/")

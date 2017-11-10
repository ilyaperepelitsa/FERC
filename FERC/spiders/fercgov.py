# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


from scrapy.linkextractors import LinkExtractor
# from scrape_jobs.items import JobItem
from scrapy.loader import ItemLoader


# for docket in dockets:

class FercgovSpider(scrapy.Spider):
    name = "fercgov"
    allowed_domains = ["elibrary.ferc.gov"]
    start_urls = ['https://elibrary.ferc.gov/idmws/search/fercgensearch.asp']
    # docket = docket
    docstart = 0
    doccoutner = 200
    docslimit = 200
    # dockets = ["CP16-17", "CP15-500"]
    dockets = ["CP16-17"]
    # search = "pipeline"
    search = ""


    def parse(self, response):

        for docket in self.dockets:

            query = FormRequest.from_response(response,
                                    formdata = {
                                                # "FROMdt" : "",
                                                # "TOdt" : "",
                                                "firstDt" : "1/1/1904",
                                                "LastDt" : "12/31/2037",
                                                "DocsStart" : str(self.docstart),
                                                "DocsLimit" : str(self.docslimit),
                                                # "SortSpec" : "filed_date desc accession_num asc",
                                                # "datefield" : "filed_date",
                                                # "dFROM" : "10/08/2017",
                                                # "dTO" : "11/08/2017",
                                                # "dYEAR" : "1",
                                                # "dMONTH" : "1",
                                                # "dDAY" : "1",
                                                "date" : "All",
                                                # "NotCategories" : "submittal,issuance",
                                                "category" : "submittal,issuance",
                                                # "category" : "submittal",
                                                # "category" : "issuance",
                                                "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                                "docket" : str(docket),
                                                "subdock_radio" : "all_subdockets",
                                                # "class" : "999",
                                                # "type" : "999",
                                                "textsearch" : str(self.search),
                                                "description" : "description",
                                                "fulltext" : "fulltext",
                                                "DocsCount" : str(self.doccoutner)},
                                    # clickdata={'name': 'commit'},
                                    callback=self.parse_query, dont_filter = True)
            query.meta["DocsStart"] = str(self.docstart)
            query.meta["docket"] = str(docket)
            query.meta["textsearch"] = str(self.search)
            query.meta["DocsCount"] = str(self.doccoutner)
            query.meta["DocsLimit"] = str(self.docslimit)

            yield query
        # pass

    def parse_query(self, response):

        # open_in_browser(response)

        page_rows = response.xpath('//tr[@bgcolor and not(@bgcolor="navy")]').extract()
        next_pages = response.xpath('//a[text()="NextPage"]').extract()

        docstart = int(response.meta["DocsStart"])
        docket = response.meta["docket"]
        search = response.meta["textsearch"]
        doccouter = int(response.meta["DocsCount"])
        docslimit = int(response.meta["DocsLimit"])

        # next_pages = LinkExtractor(allow=(),
        #                 restrict_xpaths = '//a[text()="NextPage"]',
        #                 unique = True).extract_links(response)

        # next_page = [next_page.url for next_page in next_pages]
        # next_page = [next_page.url for next_page in next_pages]

        # yield({"pew" : len(page_rows)})
        if len(next_pages) > 0:
            docstart += doccouter
            docslimit += doccouter

            new_query = FormRequest(url="https://elibrary.ferc.gov/idmws/search/results.asp",
                formdata = {
                            "firstDt" : "1/1/1904",
                            "LastDt" : "12/31/2037",
                            "DocsStart" : str(docstart),
                            "DocsLimit" : str(docslimit),
                            "date" : "All",
                            "category" : "submittal,issuance",
                            "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                            "docket" : str(docket),
                            "textsearch" : search,
                            "subdock_radio" : "all_subdockets",
                            "DocsCount" : str(doccouter)},

                # formdata = {
                #             "FROMdt" : "",
                #             "TOdt" : "",
                #             "firstDt" : "1/1/1904",
                #             "LastDt" : "12/31/2037",
                #             "DocsStart" : str(docstart),
                #             "DocsLimit" : "500",
                #             "SortSpec" : "filed_date desc accession_num asc",
                #             "datefield" : "filed_date",
                #             "dFROM" : "10/08/2017",
                #             "dTO" : "11/08/2017",
                #             "dYEAR" : "1",
                #             "dMONTH" : "1",
                #             "dDAY" : "1",
                #             "date" : "All",
                #             "NotCategories" : "submittal,issuance",
                #             "category" : "submittal,issuance",
                #             "category" : "submittal",
                #             "category" : "issuance",
                #             "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                #             "docket" : str(docket),
                #             "subdock_radio" : "all_subdockets",
                #             "class" : "999",
                #             "type" : "999",
                #             "textsearch" : "",
                #             "description" : "description",
                #             "fulltext" : "fulltext",
                #             "DocsCount" : str(doccouter)},
                # clickdata={'name': 'commit'},
                callback=self.parse_query, dont_filter = True)
            new_query.meta["DocsStart"] = str(docstart)
            new_query.meta["docket"] = str(docket)
            new_query.meta["textsearch"] = str(search)
            new_query.meta["DocsCount"] = str(doccouter)
            new_query.meta["DocsLimit"] = str(docslimit)

            yield new_query
        # yield({"pew" : dir(self)})
        # yield {"pew" : self.doccoutner}
        # yield {"pew1" : self.docstart}
        # yield {"pew2" : self.docket}
        # yield {"pew3" : self.docket}

        # yield {"pew" : self.from_crawler}
        # yield {"pew1" : self.handles_request}
        # yield {"pew2" : self.log}
        # yield {"pew" : self.logger}
        # yield {"pew1" : self.make_requests_from_url}
        # yield {"pew2" : self.parse_query}
        # yield {"pew" : self.set_crawler}
        # yield {"pew1" : self.start_requests}
        # yield {"pew2" : self.update_settings}
        # parse_query

        yield {"pew2" : [len(page_rows), docket, docstart, doccouter]}


        # open_in_browser(response)

# 15 + 167
#
# pew = ["pew", "pew2"]
# {pewval : ["submittal", "issuance"] for pewval in pew}

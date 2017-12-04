# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


from scrapy.linkextractors import LinkExtractor
# from scrape_jobs.items import JobItem
from scrapy.loader import ItemLoader
# from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
# for docket in dockets:

class FercgovSpider(scrapy.Spider):
    name = "fercgov"
    allowed_domains = ["elibrary.ferc.gov"]
    start_urls = ['https://elibrary.ferc.gov/idmws/search/fercgensearch.asp']
    # docket = docket
    docstart = 0
    doccounter = 200
    docslimit = 200
    # dockets = ["CP16-17", "CP15-500"]
    dockets = ["CP16-17"]
    # dockets = []
    # search = "pipeline"
    search = ""


    def parse(self, response):

        if len(self.dockets) > 0:

            for docket in self.dockets:

                query = FormRequest.from_response(response,
                                        # formdata = {
                                        #             # "FROMdt" : "",
                                        #             # "TOdt" : "",
                                        #             "firstDt" : "1/1/1904",
                                        #             "LastDt" : "12/31/2037",
                                        #             "DocsStart" : str(self.docstart),
                                        #             "DocsLimit" : str(self.docslimit),
                                        #             # "SortSpec" : "filed_date desc accession_num asc",
                                        #             # "datefield" : "filed_date",
                                        #             # "dFROM" : "10/08/2017",
                                        #             # "dTO" : "11/08/2017",
                                        #             # "dYEAR" : "1",
                                        #             # "dMONTH" : "1",
                                        #             # "dDAY" : "1",
                                        #             "date" : "All",
                                        #             # "NotCategories" : "submittal,issuance",
                                        #             "category" : "submittal,issuance",
                                        #             # "category" : "submittal",
                                        #             # "category" : "issuance",
                                        #             "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                        #             "docket" : str(docket),
                                        #             "subdock_radio" : "all_subdockets",
                                        #             # "class" : "999",
                                        #             # "type" : "999",
                                        #             "textsearch" : str(self.search),
                                        #             "description" : "description",
                                        #             "fulltext" : "fulltext",
                                        #             "DocsCount" : str(self.doccounter)},

                                            formdata = {
                                                        "FROMdt" : "",
                                                        "TOdt" : "",
                                                        "firstDt" : "1/1/1904",
                                                        "LastDt" : "12/31/2037",
                                                        "DocsStart" : str(self.docstart),
                                                        "DocsLimit" : str(self.docslimit),
                                                        "SortSpec" : "filed_date desc accession_num asc",
                                                        "datefield" : "filed_date",
                                                        "dFROM" : "10/08/2017",
                                                        "dTO" : "11/08/2017",
                                                        "dYEAR" : "1",
                                                        "dMONTH" : "1",
                                                        "dDAY" : "1",
                                                        "date" : "All",
                                                        # "NotCategories" : "submittal,issuance",
                                                        "category" : "submittal,issuance",
                                                        # "category" : "submittal",
                                                        # "category" : "issuance",
                                                        "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                                        "docket" : str(docket),
                                                        "subdock_radio" : "all_subdockets",
                                                        "class" : "999",
                                                        "type" : "999",
                                                        "textsearch" : str(self.search),
                                                        "description" : "description",
                                                        "fulltext" : "fulltext",
                                                        "DocsCount" : str(self.doccounter)},
                                        # clickdata={'name': 'commit'},
                                        callback=self.parse_query, dont_filter = True)
                query.meta["DocsStart"] = str(self.docstart)
                query.meta["docket"] = str(docket)
                query.meta["textsearch"] = str(self.search)
                query.meta["DocsCount"] = str(self.doccounter)
                query.meta["DocsLimit"] = str(self.docslimit)

                yield query
                # open_in_browser(response)
        else:


            query = FormRequest.from_response(response,
                                    # formdata = {
                                    #             # "FROMdt" : "",
                                    #             # "TOdt" : "",
                                    #             "firstDt" : "1/1/1904",
                                    #             "LastDt" : "12/31/2037",
                                    #             "DocsStart" : str(self.docstart),
                                    #             "DocsLimit" : str(self.docslimit),
                                    #             # "SortSpec" : "filed_date desc accession_num asc",
                                    #             # "datefield" : "filed_date",
                                    #             # "dFROM" : "10/08/2017",
                                    #             # "dTO" : "11/08/2017",
                                    #             # "dYEAR" : "1",
                                    #             # "dMONTH" : "1",
                                    #             # "dDAY" : "1",
                                    #             "date" : "All",
                                    #             # "NotCategories" : "submittal,issuance",
                                    #             "category" : "submittal,issuance",
                                    #             # "category" : "submittal",
                                    #             # "category" : "issuance",
                                    #             "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                    #             "docket" : "",
                                    #             "subdock_radio" : "all_subdockets",
                                    #             # "class" : "999",
                                    #             # "type" : "999",
                                    #             "textsearch" : str(self.search),
                                    #             "description" : "description",
                                    #             "fulltext" : "fulltext",
                                    #             "DocsCount" : str(self.doccounter)},

                                    formdata = {
                                                "FROMdt" : "",
                                                "TOdt" : "",
                                                "firstDt" : "1/1/1904",
                                                "LastDt" : "12/31/2037",
                                                "DocsStart" : str(self.docstart),
                                                "DocsLimit" : str(self.docslimit),
                                                "SortSpec" : "filed_date desc accession_num asc",
                                                "datefield" : "filed_date",
                                                "dFROM" : "10/08/2017",
                                                "dTO" : "11/08/2017",
                                                "dYEAR" : "1",
                                                "dMONTH" : "1",
                                                "dDAY" : "1",
                                                "date" : "All",
                                                # "NotCategories" : "submittal,issuance",
                                                "category" : "submittal,issuance",
                                                # "category" : "submittal",
                                                # "category" : "issuance",
                                                "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                                "docket" : "",
                                                "subdock_radio" : "all_subdockets",
                                                "class" : "999",
                                                "type" : "999",
                                                "textsearch" : str(self.search),
                                                "description" : "description",
                                                "fulltext" : "fulltext",
                                                "DocsCount" : str(self.doccounter)},
                                    # clickdata={'name': 'commit'},
                                    callback=self.parse_query, dont_filter = True)
            query.meta["DocsStart"] = str(self.docstart)
            query.meta["docket"] = ""
            query.meta["textsearch"] = str(self.search)
            query.meta["DocsCount"] = str(self.doccounter)
            query.meta["DocsLimit"] = str(self.docslimit)

            yield query
            # open_in_browser(response)
        # pass

    def parse_query(self, response):

        # open_in_browser(response)
        # hxs = HtmlXPathSelector(response)
        page_rows = response.xpath('//tr[@bgcolor and not(@bgcolor="navy")]').extract()
        # page_rows = response.xpath('//tr[@bgcolor and not(@bgcolor="navy")]')
        for row in page_rows:
            sel = Selector(text = row)
            # row_response = HtmlResponse(url = "none", body=row)
            columns = sel.xpath('body/tr/td').extract()

            ## SUBMITTAL/ISSUANCE + #
            sel2 = Selector(text = columns[0])
            text_pew = sel2.xpath("//*[not(name()='a')]/text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]

            ## SUBMITTAL/ISSUANCE DOCUMENT COMPONENTS LINK
            ##################### USELESS - SAME INFO IS CONTAINED ELSEWHERE
            sel2 = Selector(text = columns[0])
            text_pew = sel2.xpath("//a/@href").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]

            ## DOC DATE / PUBLISH DATE
            sel2 = Selector(text = columns[1])
            text_pew = sel2.xpath("//text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]

            ## DOCKET NUMBER / NUMBERS
            sel2 = Selector(text = columns[2])
            text_pew = sel2.xpath("//*[not(name()='a')]/text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]

            ## DESCRIPTION
            sel2 = Selector(text = columns[3])
            text_pew = sel2.xpath("//text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            text_pew = text_pew[0]

            ## AVAILABILITY - ONLY PUBLIC ARE DOWNLOADABLE
            sel2 = Selector(text = columns[3])
            text_pew = sel2.xpath("//text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            text_pew = text_pew[1]

            ## CLASS 
            sel2 = Selector(text = columns[4])
            text_pew = sel2.xpath("//text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            text_pew = text_pew[0]

            ## TYPE
            sel2 = Selector(text = columns[4])
            text_pew = sel2.xpath("//text()").extract()
            text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            text_pew = text_pew[1]
            # #
            # #
            # #PDF AND EXCEL LINKS - NAMES
            # sel2 = Selector(text = columns[5])
            # text_pew = sel2.xpath("//a/text()").extract()
            # text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            # text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            # text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            #
            # #PDF AND EXCEL LINKS - LINKS
            # sel2 = Selector(text = columns[5])
            # text_pew = sel2.xpath("//a/@href").extract()
            # text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            # text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            # text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            # #
            # ## FILE AND INFO TEXT
            # sel2 = Selector(text = columns[6])
            # text_pew = sel2.xpath("//a/text()").extract()
            # text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            # text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            # text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            #
            # ## FILE AND INFO LINKS
            # sel2 = Selector(text = columns[6])
            # text_pew = sel2.xpath("//a/@href").extract()
            # text_pew = [texty.replace("\r", "") for texty in text_pew if texty.replace("\r", "") != ""]
            # text_pew = [texty.replace("\n", "") for texty in text_pew if texty.replace("\n", "") != ""]
            # text_pew = [texty.replace("\t", "") for texty in text_pew if texty.replace("\t", "") != ""]
            #


            # yield {"pew2" : columns}
            yield {"pew2" : text_pew}
            # yield {"pew2" : len(columns)}


        # page_rows = response.xpath('//tr[@bgcolor and not(@bgcolor="navy")]').extract()
        next_pages = response.xpath('//a[text()="NextPage"]').extract()

        docstart = int(response.meta["DocsStart"])
        docket = response.meta["docket"]
        search = response.meta["textsearch"]
        doccounter = int(response.meta["DocsCount"])
        docslimit = int(response.meta["DocsLimit"])

        # for row in page_rows:
        #     columns = row.xpath('td').extract()
        #     yield {"pew2" : columns[0]}
            # yield {"pew2" : columns[0]}


        # next_pages = LinkExtractor(allow=(),
        #                 restrict_xpaths = '//a[text()="NextPage"]',
        #                 unique = True).extract_links(response)

        # next_page = [next_page.url for next_page in next_pages]
        # next_page = [next_page.url for next_page in next_pages]

        # yield({"pew" : len(page_rows)})
        if len(next_pages) > 0:
            docstart += doccounter
            docslimit += doccounter

            new_query = FormRequest(url="https://elibrary.ferc.gov/idmws/search/results.asp",
                # formdata = {
                #             "firstDt" : "1/1/1904",
                #             "LastDt" : "12/31/2037",
                #             "DocsStart" : str(docstart),
                #             "DocsLimit" : str(docslimit),
                #             "date" : "All",
                #             "category" : "submittal,issuance",
                #             "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                #             "docket" : str(docket),
                #             "textsearch" : search,
                #             "subdock_radio" : "all_subdockets",
                #             "DocsCount" : str(doccounter)},

                formdata = {
                            "FROMdt" : "",
                            "TOdt" : "",
                            "firstDt" : "1/1/1904",
                            "LastDt" : "12/31/2037",
                            "DocsStart" : str(docstart),
                            "DocsLimit" : str(docslimit),
                            "date" : "All",
                            "SortSpec" : "filed_date desc accession_num asc",
                            "datefield" : "filed_date",
                            "dFROM" : "10/08/2017",
                            "dTO" : "11/08/2017",
                            "dYEAR" : "1",
                            "dMONTH" : "1",
                            "dDAY" : "1",
                            "date" : "All",
                            # "NotCategories" : "submittal,issuance",
                            "category" : "submittal,issuance",
                            # "category" : "submittal",
                            # "category" : "issuance",
                            "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                            "docket" : str(docket),
                            "subdock_radio" : "all_subdockets",
                            "class" : "999",
                            "type" : "999",
                            "textsearch" : str(search),
                            "description" : "description",
                            "fulltext" : "fulltext",
                            "DocsCount" : str(doccounter)},

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
            new_query.meta["DocsCount"] = str(doccounter)
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

        # yield {"pew2" : [len(page_rows), docket, docstart, doccounter]}





        # open_in_browser(response)

# 15 + 167
#
# pew = ["pew", "pew2"]
# {pewval : ["submittal", "issuance"] for pewval in pew}

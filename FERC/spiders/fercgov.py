# -*- coding: utf-8 -*-
import uuid

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

    script = """
    function main(splash, args)

        function wait_to_load(time)
            local initial_check = true
            local initial_html = splash:html()

            while initial_check do
                assert(splash:wait(time))
                local new_html = splash:html()
                if (initial_html == new_html) then
                    initial_check = false
                else
                    initial_html = new_html
                end
            end
        end

        wait_to_load(5)

        return {
        html = splash:html()
        }

    end
    """


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

            itemdata = {}

            sel = Selector(text = row)
            # row_response = HtmlResponse(url = "none", body=row)
            columns = sel.xpath('body/tr/td').extract()

            ## SUBMITTAL/ISSUANCE + #
            sel2 = Selector(text = columns[0])
            column1 = sel2.xpath("//*[not(name()='a')]/text()").extract()
            column1 = [element.replace("\r", "") for element in column1 if element.replace("\r", "") != ""]
            column1 = [element.replace("\n", "") for element in column1 if element.replace("\n", "") != ""]
            itemdata["action_category"] = column1[0]
            itemdata["action_accession"] = column1[1]


            ## DOC DATE / PUBLISH DATE
            sel2 = Selector(text = columns[1])
            column2 = sel2.xpath("//text()").extract()
            column2 = [element.replace("\r", "") for element in column2 if element.replace("\r", "") != ""]
            column2 = [element.replace("\n", "") for element in column2 if element.replace("\n", "") != ""]
            column2 = [element.replace("\t", "") for element in column2 if element.replace("\t", "") != ""]
            itemdata["date_doc"] = column2[0]
            itemdata["date_publish"] = column2[1]
            #
            ## DOCKET NUMBER / NUMBERS
            sel2 = Selector(text = columns[2])
            column3 = sel2.xpath("//*[not(name()='a')]/text()").extract()
            column3 = [element.replace("\r", "") for element in column3 if element.replace("\r", "") != ""]
            column3 = [element.replace("\n", "") for element in column3 if element.replace("\n", "") != ""]
            column3 = [element.replace("\t", "") for element in column3 if element.replace("\t", "") != ""]
            if len(column3) == 1:
                itemdata["docket_numbers"] = column3[0]
            else:
                itemdata["docket_numbers"] = column3

            ## DESCRIPTION
            sel2 = Selector(text = columns[3])
            column4 = sel2.xpath("//text()").extract()
            column4 = [element.replace("\r", "") for element in column4 if element.replace("\r", "") != ""]
            column4 = [element.replace("\n", "") for element in column4 if element.replace("\n", "") != ""]
            column4 = [element.replace("\t", "") for element in column4 if element.replace("\t", "") != ""]
            itemdata["description"] = column4[0]
            itemdata["availability"] = column4[1].split("Availability:")[-1].strip()

            #
            ## CLASS
            sel2 = Selector(text = columns[4])
            column5 = sel2.xpath("//text()").extract()
            column5 = [element.replace("\r", "") for element in column5 if element.replace("\r", "") != ""]
            column5 = [element.replace("\n", "") for element in column5 if element.replace("\n", "") != ""]
            column5 = [element.replace("\t", "") for element in column5 if element.replace("\t", "") != ""]
            itemdata["class"] = column5[0]
            itemdata["type"] = column5[1]
            #
            # ## TYPE
            # sel2 = Selector(text = columns[4])
            # text_pew = sel2.xpath("//text()").extract()
            # text_pew = [element.replace("\r", "") for element in text_pew if element.replace("\r", "") != ""]
            # text_pew = [element.replace("\n", "") for element in text_pew if element.replace("\n", "") != ""]
            # text_pew = [element.replace("\t", "") for element in text_pew if element.replace("\t", "") != ""]
            # text_pew = text_pew[1]
            # #
            # #
            # #PDF AND EXCEL LINKS - NAMES
            # sel2 = Selector(text = columns[5])
            # text_pew = sel2.xpath("//a/text()").extract()
            # text_pew = [element.replace("\r", "") for element in text_pew if element.replace("\r", "") != ""]
            # text_pew = [element.replace("\n", "") for element in text_pew if element.replace("\n", "") != ""]
            # text_pew = [element.replace("\t", "") for element in text_pew if element.replace("\t", "") != ""]
            #
            # #PDF AND EXCEL LINKS - LINKS
            # sel2 = Selector(text = columns[5])
            # text_pew = sel2.xpath("//a/@href").extract()
            # text_pew = [element.replace("\r", "") for element in text_pew if element.replace("\r", "") != ""]
            # text_pew = [element.replace("\n", "") for element in text_pew if element.replace("\n", "") != ""]
            # text_pew = [element.replace("\t", "") for element in text_pew if element.replace("\t", "") != ""]
            # #
            ## FILE AND INFO TEXT
            sel2 = Selector(text = columns[6])
            column6_text = sel2.xpath("//a/text()").extract()
            column6_text = [element.replace("\r", "") for element in column6_text if element.replace("\r", "") != ""]
            column6_text = [element.replace("\n", "") for element in column6_text if element.replace("\n", "") != ""]
            column6_text = [element.replace("\t", "") for element in column6_text if element.replace("\t", "") != ""]

            # #
            ## FILE AND INFO LINKS
            # sel2 = Selector(text = columns[6])
            column6_link = sel2.xpath("//a/@href").extract()
            column6_link = [element.replace("\r", "") for element in column6_link if element.replace("\r", "") != ""]
            column6_link = [element.replace("\n", "") for element in column6_link if element.replace("\n", "") != ""]
            column6_link = [element.replace("\t", "") for element in column6_link if element.replace("\t", "") != ""]
            column6_link = ["https://elibrary.ferc.gov/idmws/search/" + str(element) for element in column6_link]

            links_and_text = list(zip(column6_text, column6_link))
            for element in links_and_text:
                itemdata[str(element[0]).lower() + "_link"] = element[1]

            itemdata["splash"] = {'args': {'lua_source': self.script, 'html' : 1, 'endpoint': 'execute'}}

            # yield scrapy.Request(response.url, self.parse_next_page, meta={
            #     'splash': {
            #         'args': {
            #             'lua_source': self.script,
            #             'html': 7},
            #         'endpoint': 'execute'}}, dont_filter=True)

            info_request = scrapy.Request(itemdata["info_link"],
                                            callback = self.parse_info,
                                            meta = itemdata, dont_filter = True)
            # yield info_request



            # //tbody/tr[.//font and not(.//table) and .//td[@bgcolor = "silver"] and .//*[not(.//b)]]
            # //tbody/tr[descendant::*[not(name() = "b")]]

            yield {"pew2" : itemdata["splash"]}
            # yield {"pew2" : itemdata["info_link"]}


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

    def parse_info(self, response):

        #### GOOD FOR LAST TABLES
        bottob_tables_xpath = '//table[not(.//table) and .//td and .//font and count(.//td)>1 and .//td[@bgcolor = "silver"]]'

        # LAST TABLES WITH TABLE NAME
        bottob_tables_full_xpath = '//td[not(.//table//table) and .//td and .//font and count(.//td)>1 and .//td[@bgcolor = "silver"]]/text()'

        ### GOOD FOR BASIC INFO
        basic_info_table_xpath = '//tbody/tr[.//font and not(.//table) and .//td[@bgcolor = "silver"] and ./td[not(.//b)]]'

        ### GOOD FOR BORDERLESS TABLES WITH LIB AND TYPE
        borderless_tables_xpath = '//td[.//table[.//td and .//font and not(.//td[@bgcolor = "silver"])] and count(.//table)<10]'

        pewpew = response.xpath(bottob_tables_xpath).extract()

        # yield {"pew" : response.meta}
        # filename = uuid.uuid4()
        #
        # with open('/Users/ilyaperepelitsa/quant/' + str(filename) + ".json", "w") as f:
        #     f.write(response)
        # yield {"pew" : dir(response)}
        yield {"pew" : response.body}
        # open_in_browser(response)


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

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

import re
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

            info_query = FormRequest(url = "https://elibrary.ferc.gov/idmws/doc_info.asp",
                formdata = {"doclist" : itemdata["info_link"].split("doclist=")[-1]},
                callback=self.parse_info, dont_filter = True, meta = itemdata)

            # yield {"pew2" : itemdata["info_link"].split("doclist=")[-1]}
            # yield {"pew2" : itemdata["info_link"]}
            yield info_query

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
        bottom_tables_xpath = '//table[not(.//table) and .//td and .//font and count(.//td)>1 and .//td[@bgcolor = "silver"]]'

        # LAST TABLES WITH TABLE NAME
        bottom_tables_full_xpath = '//td[not(.//table//table) and .//td and .//font and count(.//td)>1 and .//td[@bgcolor = "silver"]]'

        ### GOOD FOR BASIC INFO
        basic_info_table_xpath = '//tbody/tr[.//font and not(.//table) and .//td[@bgcolor = "silver"] and ./td[not(.//b)]]'

        ### GOOD FOR BORDERLESS TABLES WITH LIB AND TYPE
        borderless_tables_xpath = '//td[.//table[.//td and .//font and not(.//td[@bgcolor = "silver"])] and count(.//table)<10]'

        bottom_tables = response.xpath(bottom_tables_full_xpath).extract()

        document_class_type = []
        document_child_list = []
        document_parent_list = []
        associated_numbers = []
        docket_numbers = []
        output_row = {}

        for bottom_table in bottom_tables:
            sel = Selector(text = bottom_table)
            # row_response = HtmlResponse(url = "none", body=row)
            extracted_rows = sel.xpath('//tr[not(.//tr)]').extract()
            bottom_table_name = sel.xpath('//td//b//text()').extract()
            bottom_table_name = [element.replace("\r", "") for element in bottom_table_name if element.replace("\r", "") != ""]
            bottom_table_name = [element.replace("\n", "") for element in bottom_table_name if element.replace("\n", "") != ""]
            bottom_table_name = [element.replace("\t", "") for element in bottom_table_name if element.replace("\t", "") != ""]
            bottom_table_name = bottom_table_name[0]
            bottom_table_name = bottom_table_name.replace(":", "").strip()
            bottom_table_name = bottom_table_name.replace(" ", "_").upper()
            table_column_labels = []

            for position, row in enumerate(extracted_rows):
                # sel2 = Selector(text = re.sub("\<table\>.+\<\/table\>", "", row))
                sel2 = Selector(text = row)
                # extracted_text = sel2.xpath('//td//text() | //td//a//text()').extract()
                extracted_text = sel2.xpath('//td//text()').extract()
                extracted_text = [element.replace("\r", "") for element in extracted_text]
                extracted_text = [element.replace("\n", "") for element in extracted_text]
                extracted_text = [element.replace("\t", "") for element in extracted_text]

                # yield {"pew" : [response.meta["info_link"], len(extracted_text), extracted_text]}



                if position == 0:
                    table_column_labels = extracted_text
                else:
                    if bottom_table_name == "CORRESPONDENT":
                        if len(extracted_text) == 5:
                            # output_row["correspondent_type"] = bottom_table_name + "_" + extracted_text[0]
                            first_name = extracted_text[2]
                            middle_name = extracted_text[3]
                            last_name = extracted_text[1]
                            name_component_list = [first_name, middle_name, last_name]
                            for component_position, name_component in enumerate(name_component_list):
                                if name_component == "x":
                                    name_component_list[component_position] = "*"
                            full_name = ' '.join(map(str, name_component_list))
                            full_name = full_name.replace("* ", "").replace("*", "").strip()

                            name_column_label = bottom_table_name + "_" + extracted_text[0]  + "_NAME"
                            name_column_label = str(name_column_label).lower()

                            org_column_label = bottom_table_name + "_" + extracted_text[0]  + "_ORGANIZATION"
                            org_column_label = str(org_column_label).lower()

                            output_row[name_column_label] = full_name.upper()
                            output_row[org_column_label] = extracted_text[4]
                        else:
                            output_row["correspondent_type"] = bottom_table_name + "_" + extracted_text[0]
                            name_component_list = extracted_text[1:-1]
                            for component_position, name_component in enumerate(name_component_list):
                                if name_component == "x":
                                    name_component_list[component_position] = "*"
                            full_name = ' '.join(map(str, name_component_list))
                            full_name = full_name.replace("* ", "").replace("*", "").strip()

                            name_column_label = bottom_table_name + "_" + extracted_text[0]  + "_NAME"
                            name_column_label = str(name_column_label).lower()

                            org_column_label = bottom_table_name + "_" + extracted_text[0]  + "_ORGANIZATION"
                            org_column_label = str(org_column_label).lower()

                            output_row[name_column_label] = full_name.upper()
                            output_row[org_column_label] = extracted_text[-1]

                    if bottom_table_name == "DOCUMENT_TYPE":
                        class_type_row = extracted_text[0] + " - " + extracted_text[1]
                        document_class_type.append(class_type_row)

                    if bottom_table_name in ["PARENT_DOCUMENTS", "CHILD_DOCUMENTS"]:
                        extracted_text = [element for element in extracted_text if element != ""]
                        # parent_child_labels = list(map(lambda x: bottom_table_name.split("_")[0].lower() + "_" + x, table_column_labels))

                        if bottom_table_name.split("_")[0].lower() == "parent":
                            document_parent_list.append(" - ".join(extracted_text))
                        elif bottom_table_name.split("_")[0].lower() == "child":
                            document_child_list.append(" - ".join(extracted_text))

                    if bottom_table_name == "ASSOCIATED_NUMBERS":
                        extracted_text = [element for element in extracted_text if element != ""]
                        associated_numbers_row = " - ".join(extracted_text)
                        associated_numbers.append(associated_numbers_row)

                    if bottom_table_name == "DOCKET_NUMBERS":
                        extracted_text = [element for element in extracted_text if element != ""]

                        docket_numbers_row = "-".join(extracted_text[0:-1])
                        docket_numbers_row = " : ".join([docket_numbers_row, extracted_text[-1]])
                        docket_numbers.append(docket_numbers_row)
                    # if bottom_table_name not in ["DOCKET_NUMBERS", "ASSOCIATED_NUMBERS",
                    #         "PARENT_DOCUMENTS", "CHILD_DOCUMENTS", "DOCUMENT_TYPE", "CORRESPONDENT"]:



                        # yield {"pew" : [response.meta["info_link"], bottom_table_name]}



            # yield {"pew" : [response.meta["info_link"], bottom_table_name]}
        document_class_type = ", ".join(document_class_type)
        document_parent_list = ", ".join(document_parent_list)
        document_child_list = ", ".join(document_child_list)
        associated_numbers = ", ".join(associated_numbers)
        docket_numbers = ", ".join(docket_numbers)

        output_row["document_class_type"] = document_class_type
        output_row["document_child_list"] = document_child_list
        output_row["document_parent_list"] = document_parent_list
        output_row["associated_numbers"] = associated_numbers
        output_row["docket_numbers"] = docket_numbers


        borderless_tables = response.xpath(borderless_tables_xpath).extract()

        for borderless_table in borderless_tables:
            sel = Selector(text = borderless_table)
            # row_response = HtmlResponse(url = "none", body=row)
            borderless_table_name = sel.xpath('//b//text()').extract()
            borderless_table_content = sel.xpath('//tr//text()').extract()

            yield {"pew" : [response.meta["info_link"], borderless_table_name, borderless_table_content]}

            borderless_table_name = [element.replace("\r", "") for element in borderless_table_name if element.replace("\r", "") != ""]
            borderless_table_name = [element.replace("\n", "") for element in borderless_table_name if element.replace("\n", "") != ""]
            borderless_table_name = [element.replace("\t", "") for element in borderless_table_name if element.replace("\t", "") != ""]

            borderless_table_content = [element.replace("\r", "") for element in borderless_table_content if element.replace("\r", "") != ""]
            borderless_table_content = [element.replace("\n", "") for element in borderless_table_content if element.replace("\n", "") != ""]
            borderless_table_content = [element.replace("\t", "") for element in borderless_table_content if element.replace("\t", "") != ""]



        basic_info_rows = response.xpath(basic_info_table_xpath).extract()

        for basic_info_row in basic_info_rows:
            sel = Selector(text = basic_info_row)
            # row_response = HtmlResponse(url = "none", body=row)
            basic_info_entry = sel.xpath('/td//text()').extract()
            borderless_table_content = sel.xpath('//tr//text()').extract()

            
        # yield {"pew" : [response.meta["info_link"], len(document_class_type)]}
        # yield {"pew" : [response.meta["info_link"], output_row]}
        # yield {"pew" : [response.meta["info_link"], output_row["docket_numbers"]]}
        # yield {"pew" : [response.meta["info_link"], len(output_row["document_class_type"].split(","))]}


            # yield {"pew" : [response.meta["info_link"], bottom_table_name]}
                        # yield {"pew" : extracted_text}


        # yield {"pew" : response.meta}
        # filename = uuid.uuid4()
        #
        # with open('/Users/ilyaperepelitsa/quant/' + str(filename) + ".json", "w") as f:
        #     f.write(response)
        # yield {"pew" : dir(response)}
        # yield {"pew" : len(pewpew)}
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


pewpew = ["a", "b", "c"]
pew2 = "-".join(pewpew[0:-1])
" - ".join([pew2, pewpew[-1]])
        # open_in_browser(response)

# stringy = """<td colspan="4">\r\n\t<table width="500" cellpadding="2" align="center" border="1">\r\n\t\t<font face="arial" size="2"><b><u>Parent Documents: </u></b>\r\n\t\t<tr>\r\n\t\t<td width="150" bgcolor="silver"><font face="ARIAL" size="2"><b>Accession Number: </b></font></td>\r\n\t\t<td bgcolor="silver"><font face="ARIAL" size="2"><b>Description: </b></font></td>\r\n\t\t</tr>\r\n\t\t<tr>\r\n\t\t<td width="150"><font face="ARIAL" size="2">\r\n\t\t<a href="doc_info.asp?document_id=14621180">20171120-0015</a>\r\n\t\t</font>\r\n\t\t</td>\r\n\t\t<td><font face="ARIAL" size="2">The State of New York Office of the Attorney General submits three copies of the "Petition for Review of Two FERC Orders" with Exhibits A and B etc. under CP16-17. Part 1 of 6</font></td>\r\n\t\t</tr>\r\n\t</font></table>\r\n\t<br>\r\n\t\r\n\r\n</td>"""
#
# re.sub("\<table\>(.+)\<\/table\>", "", stringy)

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
import json


class FercgovSpider(scrapy.Spider):
    """
    Variables___________________

    GENERAL WARNING ABOUT docstart, docslimit, doccounter:
            empirically it was discovered that the server can produce
            more than 200 in search results. 200 is very stable though
            and this scraper has a replicated (reverse-engineered) way
            that the server increments its counters for "next pages".

    FORMATTING OF VARIABLES THAT NEED TO BE CHANGED:
            If you're not familiar with Python syntax, all options are provided
            below. If you need to use a list for dockets - there is an example
            of how to pass a list. If you want no dockets specified, uncomment
            the line that has an empty list (delete the "#" symbol at the line start).
            Please use those particular formats. Make sure that both "dockets"
            and "search" variables are declared (at least one of the provided
            formatting options is uncommented and filled with the search data
            that you want).



    +++ Variables that can't be changed:
            - name: scraper name that is called by [scrapy crawl] command.
                    cd into this project directory (FERC) and TYPE
                    "scrapy crawl fercgov" to start the scrapers

            - allowed_domains: only pages that have their url contain this
                    domain are considered as appropriate [response]. Generated
                    automatically by scrapy. If changed, none of the returned
                    pages will be processed

            - start_urls: url that requests are sent to. FERC has a very unique
                    way of displaying pages. In order to see any new page this
                    scraper sends HTTP POST requests to the FERC server.

            - docstart: first document to be contained in output in the search
                    results

            - doccounter: increment the "next page" requests and get this many
                    of next documents

            - docslimit: last document to be contained in output in the search
                    results

    +++ Variables that need to be changed according to your needs:
            - dockets: list of dockets to be searched. Has to be a list regardless
                    of the number of dockets (whether it's many dockets written
                    as a list of strings or no specific docket written as an
                    empty list).

                    Acceptable formats:
                    ["########", "########"] - search for many dockets in separate
                            queries
                    ["########"] - search one docket
                    [] - docket not specified (search by text instead)

            - search: string containing the word/phrase to search by.

                    Acceptable formats:
                    "########" - search for a string pattern either alongside
                            specific dockets or by itself
                    "" - don't include a string in the query. Requires having one
                            or more dockets
    """

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

        # If the docket list isn't empty
        if len(self.dockets) > 0:

            # For each docket generate a new search request
            for docket in self.dockets:

                # Query request declared with all the search data
                # formdata includes the data that FERC server accepts
                query = FormRequest.from_response(response,
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
                                "category" : "submittal,issuance",
                                "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                "docket" : str(docket),
                                "subdock_radio" : "all_subdockets",
                                "class" : "999",
                                "type" : "999",
                                "textsearch" : str(self.search),
                                "description" : "description",
                                "fulltext" : "fulltext",
                                "DocsCount" : str(self.doccounter)},
                callback=self.parse_query, dont_filter = True)
                # pass the relevant form data to the query for parsing next pages
                # and generating new queries
                query.meta["DocsStart"] = str(self.docstart)
                query.meta["docket"] = str(docket)
                query.meta["textsearch"] = str(self.search)
                query.meta["DocsCount"] = str(self.doccounter)
                query.meta["DocsLimit"] = str(self.docslimit)
                # query posted to the server
                yield query
        # If the docket list is empty
        else:
            # Query request declared with all the search data
            # formdata includes the data that FERC server accepts
            # since the docket is not passed, text search field is used
            query = FormRequest.from_response(response,
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
                                "category" : "submittal,issuance",
                                "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                "docket" : "",
                                "subdock_radio" : "all_subdockets",
                                "class" : "999",
                                "type" : "999",
                                "textsearch" : str(self.search),
                                "description" : "description",
                                "fulltext" : "fulltext",
                                "DocsCount" : str(self.doccounter)},
                    callback=self.parse_query, dont_filter = True)
            # pass the relevant form data to the query for parsing next pages
            # and generating new queries
            query.meta["DocsStart"] = str(self.docstart)
            query.meta["docket"] = ""
            query.meta["textsearch"] = str(self.search)
            query.meta["DocsCount"] = str(self.doccounter)
            query.meta["DocsLimit"] = str(self.docslimit)
            # query posted to the server
            yield query

    def parse_query(self, response):
        # Extract all the rows that the search results return
        # output rows are not styled and it's the easiest way to identfy them
        page_rows = response.xpath('//tr[@bgcolor and not(@bgcolor="navy")]').extract()
        # Each row contains both meta data and urls for new requests
        for row in page_rows:
            # Each observation is an item. Item data is populated in a dictionary
            itemdata = {}
            # New selector is declared to select columns for each row
            sel = Selector(text = row)
            # Use the selector to extract columns (<td>)
            columns = sel.xpath('body/tr/td').extract()

            ## SUBMITTAL/ISSUANCE + #
            sel2 = Selector(text = columns[0])
            # Select the text of any descendant except the link tags
            column1 = sel2.xpath("//*[not(name()='a')]/text()").extract()
            # Replace the new lines and other white space
            column1 = [element.replace("\r", "") for element in column1 if element.replace("\r", "") != ""]
            column1 = [element.replace("\n", "") for element in column1 if element.replace("\n", "") != ""]
            # itemdata["action_category"] = column1[0]
            # itemdata["action_accession"] = column1[1]


            ## DOC DATE / PUBLISH DATE
            sel2 = Selector(text = columns[1])
            # Select all text descendants
            column2 = sel2.xpath("//text()").extract()
            # Replace the new lines and other white space
            column2 = [element.replace("\r", "") for element in column2 if element.replace("\r", "") != ""]
            column2 = [element.replace("\n", "") for element in column2 if element.replace("\n", "") != ""]
            column2 = [element.replace("\t", "") for element in column2 if element.replace("\t", "") != ""]
            # itemdata["date_doc"] = column2[0]
            # itemdata["date_publish"] = column2[1]
            #
            ## DOCKET NUMBER / NUMBERS
            sel2 = Selector(text = columns[2])
            # Select the text of any descendant except the link tags
            column3 = sel2.xpath("//*[not(name()='a')]/text()").extract()
            # Replace the new lines and other white space
            column3 = [element.replace("\r", "") for element in column3 if element.replace("\r", "") != ""]
            column3 = [element.replace("\n", "") for element in column3 if element.replace("\n", "") != ""]
            column3 = [element.replace("\t", "") for element in column3 if element.replace("\t", "") != ""]
            # if len(column3) == 1:
            #     itemdata["docket_numbers"] = column3[0]
            # else:
            #     itemdata["docket_numbers"] = column3

            ## DESCRIPTION
            sel2 = Selector(text = columns[3])
            # Select all text descendants
            column4 = sel2.xpath("//text()").extract()
            # Replace the new lines and other white space
            column4 = [element.replace("\r", "") for element in column4 if element.replace("\r", "") != ""]
            column4 = [element.replace("\n", "") for element in column4 if element.replace("\n", "") != ""]
            column4 = [element.replace("\t", "") for element in column4 if element.replace("\t", "") != ""]
            itemdata["description"] = column4[0]
            # itemdata["availability"] = column4[1].split("Availability:")[-1].strip()

            #
            ## CLASS
            sel2 = Selector(text = columns[4])
            # Select all text descendants
            column5 = sel2.xpath("//text()").extract()
            # Replace the new lines and other white space
            column5 = [element.replace("\r", "") for element in column5 if element.replace("\r", "") != ""]
            column5 = [element.replace("\n", "") for element in column5 if element.replace("\n", "") != ""]
            column5 = [element.replace("\t", "") for element in column5 if element.replace("\t", "") != ""]
            # itemdata["class"] = column5[0]
            # itemdata["type"] = column5[1]

            ## FILE AND INFO TEXT
            sel2 = Selector(text = columns[6])
            column6_text = sel2.xpath("//a/text()").extract()
            # Replace the new lines and other white space
            column6_text = [element.replace("\r", "") for element in column6_text if element.replace("\r", "") != ""]
            column6_text = [element.replace("\n", "") for element in column6_text if element.replace("\n", "") != ""]
            column6_text = [element.replace("\t", "") for element in column6_text if element.replace("\t", "") != ""]

            # #
            ## FILE AND INFO LINKS
            column6_link = sel2.xpath("//a/@href").extract()
            # Replace the new lines and other white space
            column6_link = [element.replace("\r", "") for element in column6_link if element.replace("\r", "") != ""]
            column6_link = [element.replace("\n", "") for element in column6_link if element.replace("\n", "") != ""]
            column6_link = [element.replace("\t", "") for element in column6_link if element.replace("\t", "") != ""]
            column6_link = ["https://elibrary.ferc.gov/idmws/search/" + str(element) for element in column6_link]

            links_and_text = list(zip(column6_text, column6_link))
            for element in links_and_text:
                itemdata[str(element[0]).lower() + "_link"] = element[1]

            itemdata["query_docstart"] = response.meta["DocsStart"]
            itemdata["query_docscount"] = response.meta["DocsCount"]
            itemdata["query_docslimit"] = response.meta["DocsLimit"]
            itemdata["query_docket"] = response.meta["docket"]
            itemdata["query_textsearch"] = response.meta["textsearch"]


            # Generate a request to the server for the document info page
            # server accepts the doclist code in the form field
            info_query = FormRequest(url = "https://elibrary.ferc.gov/idmws/doc_info.asp",
                formdata = {"doclist" : itemdata["info_link"].split("doclist=")[-1]},
                callback=self.parse_info, dont_filter = True, meta = itemdata)
            yield info_query


        # Look for link to the "Next page" - the link itself isn't callable,
        # however the new request will be generated to the search query server
        # to replicate the following of such link in a browser
        next_pages = response.xpath('//a[text()="NextPage"]').extract()

        # Inherit the meta data from the previous request for new request.
        # Extract the numbers for what results to display and the query terms
        # such as dockets and search string
        docstart = int(response.meta["DocsStart"])
        docket = response.meta["docket"]
        search = response.meta["textsearch"]
        doccounter = int(response.meta["DocsCount"])
        docslimit = int(response.meta["DocsLimit"])

        # If the "Next page" link is found
        if len(next_pages) > 0:
            # Increment the nubmers for document counts so that unseen results
            # are displayed.
            docstart += doccounter
            docslimit += doccounter

            # Create a new request based on incremented and inhereted query
            # parameters
            new_query = FormRequest(url="https://elibrary.ferc.gov/idmws/search/results.asp",
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
                                "category" : "submittal,issuance",
                                "libraryall" : "electric, hydro, gas, rulemaking, oil, general",
                                "docket" : str(docket),
                                "subdock_radio" : "all_subdockets",
                                "class" : "999",
                                "type" : "999",
                                "textsearch" : str(search),
                                "description" : "description",
                                "fulltext" : "fulltext",
                                "DocsCount" : str(doccounter)},
                    callback=self.parse_query, dont_filter = True)
            # pass the relevant meta data for another loop of "Next page"
            new_query.meta["DocsStart"] = str(docstart)
            new_query.meta["docket"] = str(docket)
            new_query.meta["textsearch"] = str(search)
            new_query.meta["DocsCount"] = str(doccounter)
            new_query.meta["DocsLimit"] = str(docslimit)
            # Issue the POST request to the server
            yield new_query

    def parse_info(self, response):

        # yield response.meta
        #### Bottom tables in the Info page such as dockets, correspondents etc.
        bottom_tables_xpath = '//table[not(.//table) and .//td and .//font and count(.//td)>1 and .//td[@bgcolor = "silver"]]'

        #### Bottom tables in the Info page such as dockets, correspondents etc.
        # Includes the table name so that tables are not parsed blindly (create
        # a new field for each row) but a special formatting is applied to each
        # kind of table by name
        bottom_tables_full_xpath = '//td[not(.//table//table) and .//td and .//font and count(.//td)>1 and .//td[@bgcolor = "silver"]]'

        ### Basic meta info however more detailed than the general query
        basic_info_table_xpath = '//tbody//tr[.//font and not(.//table) and .//td[@bgcolor = "silver"] and ./td[not(.//b)]]'

        ### Borderless tables in the info page that contain library data and
        # category data
        borderless_tables_xpath = '//td[.//table[.//td and .//font and not(.//td[@bgcolor = "silver"])] and count(.//table)<10]'

        # Start parsing the page with the most information-intensive tables
        # Extract all the tables with their names
        bottom_tables = response.xpath(bottom_tables_full_xpath).extract()

        # Declare lists to store data found in the tables
        document_class_type = []
        document_child_list = []
        document_parent_list = []
        associated_numbers = []
        docket_numbers = []
        output_row = {}

        # Iterate over each extracted table
        for bottom_table in bottom_tables:
            # New selector is declared to select rows in each table
            sel = Selector(text = bottom_table)
            # Extract the rows and table name separately
            extracted_rows = sel.xpath('//tr[not(.//tr)]').extract()
            bottom_table_name = sel.xpath('//td//b//text()').extract()
            # Replace the new lines and other white space
            bottom_table_name = [element.replace("\r", "") for element in bottom_table_name if element.replace("\r", "") != ""]
            bottom_table_name = [element.replace("\n", "") for element in bottom_table_name if element.replace("\n", "") != ""]
            bottom_table_name = [element.replace("\t", "") for element in bottom_table_name if element.replace("\t", "") != ""]
            # Select the first occurance of bold text after irrelevant
            # data was dropped or replaced
            bottom_table_name = bottom_table_name[0]
            # Drop the punctuation
            bottom_table_name = bottom_table_name.replace(":", "").strip()
            # Format to filter the tables in further steps
            bottom_table_name = bottom_table_name.replace(" ", "_").upper()
            # create an empty list to store column labels
            table_column_labels = []

            # Iterate over extracted rows
            for position, row in enumerate(extracted_rows):
                # Declare a selector to parse columns
                sel2 = Selector(text = row)
                # Extract the text from each column in a row
                extracted_text = sel2.xpath('//td//text()').extract()
                # Replace the new lines and other white space
                extracted_text = [element.replace("\r", "") for element in extracted_text]
                extracted_text = [element.replace("\n", "") for element in extracted_text]
                extracted_text = [element.replace("\t", "") for element in extracted_text]

                # The first row contains
                if position == 0:
                    # Pass the column labels to list declared above
                    table_column_labels = extracted_text
                # Parse every row after the column label row
                else:
                    # Parse the table with name CORRESPONDENT
                    if bottom_table_name == "CORRESPONDENT":
                        # Most consistent version of table formatting (on the
                        # FERC side). Usually empty name fields are marked with
                        # "x" or "*", this portion of code deals with such formatting
                        if len(extracted_text) == 5:
                            # Select name fields according to their correct
                            # absolute position (index)
                            first_name = extracted_text[2]
                            middle_name = extracted_text[3]
                            last_name = extracted_text[1]
                            # Declare list with name components First, Middle, Last
                            name_component_list = [first_name, middle_name, last_name]
                            # The most common formatting for empty name field is
                            # "*", default to this method
                            for component_position, name_component in enumerate(name_component_list):
                                if name_component == "x":
                                    name_component_list[component_position] = "*"
                            # Join the name to one string since first or middle
                            # name are not essential to analysis
                            full_name = ' '.join(map(str, name_component_list))
                            # Replace "*"
                            full_name = full_name.replace("* ", "").replace("*", "").strip()

                            # Create a column label according to the type of
                            # correspondent
                            name_column_label = bottom_table_name + "_" + extracted_text[0]  + "_NAME"
                            name_column_label = str(name_column_label).lower()

                            # Create a column label according to the name of
                            # correspondent's organization name
                            org_column_label = bottom_table_name + "_" + extracted_text[0]  + "_ORGANIZATION"
                            org_column_label = str(org_column_label).lower()

                            # Default name formatting is set to uppercase (there
                            # are some inconsistencies on FERC side using either
                            # uppercase or capitalized or lowercase)
                            output_row[name_column_label] = full_name.upper()
                            output_row[org_column_label] = extracted_text[4]
                        # Less consistent version of name formatting uses empty
                        # string rather then "x" or "*", therefore no text is
                        # extracted and relative indexing has to be used
                        else:
                            output_row["correspondent_type"] = bottom_table_name + "_" + extracted_text[0]
                            # Get the name using relative indexing
                            name_component_list = extracted_text[1:-1]
                            # The most common formatting for empty name field is
                            # "*", default to this method
                            for component_position, name_component in enumerate(name_component_list):
                                if name_component == "x":
                                    name_component_list[component_position] = "*"
                            # Join the name to one string since first or middle
                            # name are not essential to analysis
                            full_name = ' '.join(map(str, name_component_list))
                            # Replace "*"
                            full_name = full_name.replace("* ", "").replace("*", "").strip()

                            # Create a column label according to the type of
                            # correspondent
                            name_column_label = bottom_table_name + "_" + extracted_text[0]  + "_NAME"
                            name_column_label = str(name_column_label).lower()

                            # Create a column label according to the name of
                            # correspondent's organization name
                            org_column_label = bottom_table_name + "_" + extracted_text[0]  + "_ORGANIZATION"
                            org_column_label = str(org_column_label).lower()

                            # Default name formatting is set to uppercase (there
                            # are some inconsistencies on FERC side using either
                            # uppercase or capitalized or lowercase)
                            output_row[name_column_label] = full_name.upper()
                            output_row[org_column_label] = extracted_text[-1]

                    # Parse the table with name DOCUMENT_TYPE
                    if bottom_table_name == "DOCUMENT_TYPE":
                        # Separate the class and type with " - "
                        class_type_row = extracted_text[0] + " - " + extracted_text[1]
                        # Store multiple document types in a list
                        # Many document submissions/issuances have more than
                        # one type/class
                        document_class_type.append(class_type_row)

                    # Parse the table with names PARENT_DOCUMENTS and CHILD_DOCUMENTS
                    # Few submissions/issuances have these hieararchical tables
                    if bottom_table_name in ["PARENT_DOCUMENTS", "CHILD_DOCUMENTS"]:
                        # Drop empty text fields
                        extracted_text = [element for element in extracted_text if element != ""]

                        # Append the lists of parent/child documents according
                        # to the listed hierarchy type
                        if bottom_table_name.split("_")[0].lower() == "parent":
                            document_parent_list.append(" - ".join(extracted_text))
                        elif bottom_table_name.split("_")[0].lower() == "child":
                            document_child_list.append(" - ".join(extracted_text))

                    # Parse the table with name ASSOCIATED_NUMBERS
                    if bottom_table_name == "ASSOCIATED_NUMBERS":
                        # Drop empty text fields
                        extracted_text = [element for element in extracted_text if element != ""]
                        associated_numbers_row = " - ".join(extracted_text)
                        associated_numbers.append(associated_numbers_row)

                    # Parse the table with name DOCKET_NUMBERS
                    if bottom_table_name == "DOCKET_NUMBERS":
                        # Drop empty text fields
                        extracted_text = [element for element in extracted_text if element != ""]
                        # Join the docket and subdocket in one string
                        docket_numbers_row = "-".join(extracted_text[0:-1])
                        # Join the full docket string with the docket type
                        docket_numbers_row = " : ".join([docket_numbers_row, extracted_text[-1]])
                        # Append the list of dockets with all subdockets
                        # It is not very common but there are issuances with a
                        # substantially large list of dockets
                        docket_numbers.append(docket_numbers_row)
                    # if bottom_table_name not in ["DOCKET_NUMBERS", "ASSOCIATED_NUMBERS",
                    #         "PARENT_DOCUMENTS", "CHILD_DOCUMENTS", "DOCUMENT_TYPE", "CORRESPONDENT"]:
                        # yield {"pew" : [response.meta["info_link"], bottom_table_name]}



            # yield {"pew" : [response.meta["info_link"], bottom_table_name]}

        # Join each list of strings into one large string
        # This is done to avoid having too many columns. For example in a case
        # when a few dozen dockets are listed in one issuance, having a column
        # for each with result in a sparse matrix with low interpretabiltiy
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

            # yield {"pew" : [response.meta["info_link"], borderless_table_name, borderless_table_content]}
            # Replace the new lines and other white space
            borderless_table_name = [element.replace("\r", "") for element in borderless_table_name if element.replace("\r", "").strip() != ""]
            borderless_table_name = [element.replace("\n", "") for element in borderless_table_name if element.replace("\n", "").strip() != ""]
            borderless_table_name = [element.replace("\t", "") for element in borderless_table_name if element.replace("\t", "").strip() != ""]
            # Replace the new lines and other white space
            borderless_table_content = [element.replace("\r", "") for element in borderless_table_content if element.replace("\r", "").strip() != ""]
            borderless_table_content = [element.replace("\n", "") for element in borderless_table_content if element.replace("\n", "").strip() != ""]
            borderless_table_content = [element.replace("\t", "") for element in borderless_table_content if element.replace("\t", "").strip() != ""]
            # Format entries and append to itemdata
            for content_element in borderless_table_content:
                borderless_table_name = "".join(borderless_table_name)
                borderless_table_name = borderless_table_name.replace(":", "")
                borderless_table_name = borderless_table_name.strip()
                borderless_table_name = borderless_table_name.lower()
                output_row[borderless_table_name + "_" + content_element.lower()] = "X"




        basic_info_rows = response.xpath(basic_info_table_xpath).extract()


        for basic_info_row in basic_info_rows:
            sel = Selector(text = basic_info_row)
            # Extract all column text
            basic_info_entry = sel.xpath('//td//text()').extract()
            # Replace all white space  and discard &nbsp
            basic_info_entry = [element.replace("\r", "") for element in basic_info_entry if element.replace("\r", "").strip() != ""]
            basic_info_entry = [element.replace("\n", "") for element in basic_info_entry if element.replace("\n", "").strip() != ""]
            basic_info_entry = [element.replace("\t", "") for element in basic_info_entry if element.replace("\t", "").strip() != ""]
            basic_info_entry = [element.replace("\t", "") for element in basic_info_entry if element.replace("\t", "").strip() != "&nbsp"]
            basic_info_entry = [element.strip() for element in basic_info_entry]
            # Split full row list into lists of 2 (column label + value)
            basic_info_entry = [basic_info_entry[i:i+2] for i in range(0,len(basic_info_entry),2)]
            # Iterate over each column label + value pair
            for entry in basic_info_entry:
                # Some instances of First Received Date being blank were observed.
                # Index out of range error is produced every time it occurs since
                # the column + value pair list that is yielded is of length = 1
                # i.e. only label is returned
                try:
                    # Set column label to lowercase, replace punctuation and
                    # white space. Do not do the same to values since white space
                    # is used to separate dates and time, PM and other important
                    # components
                    entry_label = entry[0].lower()
                    entry_label = entry_label.replace("-", "_")
                    entry_label = entry_label.replace(" ", "_")
                    entry_label = entry_label.replace(":", "")
                    output_row[entry_label] = entry[1]
                    # yield {"pew" : [response.meta["info_link"], entry_label, output_row[entry_label]]}
                except IndexError:
                    pass

        output_row["query_docstart"] = response.meta["query_docstart"]
        output_row["query_docscount"] = response.meta["query_docscount"]
        output_row["query_docslimit"] = response.meta["query_docslimit"]
        output_row["query_docket"] = response.meta["query_docket"]
        output_row["query_textsearch"] = response.meta["query_textsearch"]
        output_row["info_link"] = response.meta["info_link"]
        output_row["file_link"] = response.meta["file_link"]



        file_query = FormRequest(url = "https://elibrary.ferc.gov/idmws/file_list.asp",
            formdata = {"doclist" : output_row["info_link"].split("doclist=")[-1]},
            callback=self.parse_files, dont_filter = True, meta = output_row)

        yield file_query
        #

        # yield {"pew" : output_row}

    def parse_files(self, response):

        json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'test.json')

        item_data = response.meta
        # Delete the meta data that is not used
        drop_meta = ["download_latency", "download_slot", "download_timeout",
                        "depth"]
        for drop_item in drop_meta:
            del item_data[drop_item]

        #
        try:
            with open(json_dir) as f:
                data = json.load(f)
            if item_data["info_link"].split("doclist=")[-1] not in data.keys():
                data.update({item_data["info_link"].split("doclist=")[-1]: item_data})
        except FileNotFoundError:
            data = {item_data["info_link"].split("doclist=")[-1]: item_data}

        with open(json_dir, 'w') as f:
            json.dump(data, f)
        #
        # # yield item_data

        # with open('test.json', 'a') as f:
        #     json.dump({output_row["info_link"].split("doclist=")[-1]: item_data}, f)

        # yield {"pew" : item_data}
        # yield {"pew" : "pew"}


    #### Botto

# with open('test1.json') as f:
#     data = json.load(f)
            #
#
# pewpew = {"a" : 1, "b" : 2}
# "a" in pewpew.keys()
#
# pew
        # yield {"pew" : [response.meta["info_link"], len(document_class_type)]}
        # yield {"pew" : [response.meta["info_link"], output_row]}
        # yield {"pew" : [response.meta["info_link"], output_row["docket_numbers"]]}
        # yield {"pew" : [response.meta["info_link"], len(output_row["document_class_type"].split(","))]}
            # yield {"pew" : [response.meta["info_link"], basic_info_entry, borderless_table_content]}

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



# stringy = """<td colspan="4">\r\n\t<table width="500" cellpadding="2" align="center" border="1">\r\n\t\t<font face="arial" size="2"><b><u>Parent Documents: </u></b>\r\n\t\t<tr>\r\n\t\t<td width="150" bgcolor="silver"><font face="ARIAL" size="2"><b>Accession Number: </b></font></td>\r\n\t\t<td bgcolor="silver"><font face="ARIAL" size="2"><b>Description: </b></font></td>\r\n\t\t</tr>\r\n\t\t<tr>\r\n\t\t<td width="150"><font face="ARIAL" size="2">\r\n\t\t<a href="doc_info.asp?document_id=14621180">20171120-0015</a>\r\n\t\t</font>\r\n\t\t</td>\r\n\t\t<td><font face="ARIAL" size="2">The State of New York Office of the Attorney General submits three copies of the "Petition for Review of Two FERC Orders" with Exhibits A and B etc. under CP16-17. Part 1 of 6</font></td>\r\n\t\t</tr>\r\n\t</font></table>\r\n\t<br>\r\n\t\r\n\r\n</td>"""
#
# re.sub("\<table\>(.+)\<\/table\>", "", stringy)

# pew1 = ["pew1"]
# pew2 = ["pew3"]
#
# list(zip(pew1, pew2))
# import itertools
# list(itertools.product(pew1, pew2))
import pandas as pd
# import os
# basePath = os.path.dirname(os.path.abspath("__file__"))
# basePath
# test_df = pd.read_json("/Users/ilyaperepelitsa/quant/FERC/test.json", orient = "index")
# test_df.to_csv("/Users/ilyaperepelitsa/quant/FERC/test.csv")
# test_df.shape

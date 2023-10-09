import json

from bs4 import BeautifulSoup
from lxml import etree, html
from requests import request


def decoder(html_as_tree_object):
    number_of_tab = len(html_as_tree_object.xpath("/html/body/nav/div")[0])
    total_data = {}
    for tab_number in range(1, number_of_tab + 1):
        tab_name = html_as_tree_object.xpath(f"/html/body/nav/div/a[{tab_number}]/p/text()")[0]
        tab_data = tab_extraction(tab_name, html_as_tree_object)
        total_data[tab_name] = tab_data
    print(total_data)
    return total_data


def tab_extraction(tab_name, html_as_tree_object):
    tab_data = None
    if tab_name == "Sanctions":
        tab_data = extract_sanction_tab(html_as_tree_object)
    elif tab_name == "":
        pass
    else:
        pass
    return tab_data


def extract_sanction_tab(html_as_tree_object):
    ship_compliance = html_as_tree_object.xpath("/html/body/div/div[1]/div/div[2]/div")  # left and right column
    tables_data = {}
    for column_number in range(1,
                               len(ship_compliance) + 1):  # category    #left and right column. 1 is right and 2 is left
        number_of_table = len(
            html_as_tree_object.xpath(
                f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/div"))  # number of table in each column
        have_table_name_with_span_tag = False
        span_tag_number = 1
        bold_text_tag_number = 0
        for table_id in range(1, number_of_table + 1):  # table(title) in each column
            table_name = html_as_tree_object.xpath(
                f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/span[{span_tag_number}]/text()")
            number_of_key_or_value_in_each_table = len(
                html_as_tree_object.xpath(f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/div[{table_id}]/div"))

            if table_name:
                span_tag_number += 1
            else:
                bold_text_tag_number += 1
                table_name = html_as_tree_object.xpath(
                    f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/b[{bold_text_tag_number}]/text()")
            record = {}
            for id_of_key_or_value_in_each_table in range(1,
                                                          number_of_key_or_value_in_each_table + 1):  # key and value of each record in specific table
                if id_of_key_or_value_in_each_table % 2 == 1:
                    key = html_as_tree_object.xpath(
                        f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/div[{table_id}]/div[{id_of_key_or_value_in_each_table}]/label/text()")
                    if key:
                        key = key[0]
                    else:
                        try:
                            key = html_as_tree_object.xpath(
                                f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/div[{table_id}]/div[{id_of_key_or_value_in_each_table}]")[
                                0]
                            str_txt = key.text
                            key = str_txt.split('\r')[0]
                        except:
                            key = "cant obtain key"
                else:
                    value = html_as_tree_object.xpath(
                        f"/html/body/div/div[1]/div/div[2]/div[{column_number}]/div[{table_id}]/div[{id_of_key_or_value_in_each_table}]/span/text()")[
                        0]
                    record.update({key: value})
            tables_data[table_name[0]] = record
    return tables_data


def get_html_context_v1(html_pass):
    with open(html_pass, "r") as file:
        page = file.read()
    tree = html.fromstring(page)
    return tree


def get_html_context_v2(html_pass):
    parser = etree.HTMLParser()
    tree = etree.parse(html_pass, parser)
    return tree


def get_html_context_v3(session, url, headers, proxy):
    res = session.request("GET", url, headers=headers, proxies=proxy)
    tree = html.fromstring(res.content)
    return tree


if __name__ == '__main__':
    html_pass = r"C:\Users\o.\Desktop\tes.html"
    # html_pass = r"C:\Users\o.\Desktop\MIRS Ship Details.mhtml"

    # html_as_tree_object = get_html_context_v1(html_pass)
    html_as_tree_object = get_html_context_v2(html_pass)
    # html_as_tree_object = get_html_context_v3(session, url, headers, proxy)
    decoder(html_as_tree_object)

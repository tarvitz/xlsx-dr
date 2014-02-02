""" Bydlo xlsx file parsers

.. module:: xlsx
    :platform: Linux, Unix, Windows
    :synopsis: bydlo xlsx file parser for urgent and 'unclean' needs

.. moduleauthor:: You'd better not know

"""
# coding: utf-8
import re
import os
from openpyxl import load_workbook
import simplejson as json
from helpers import encoder
from lxml import etree
from zipfile import ZipFile


class XlsxReader(object):
    """ XlsxReader - dirty xlsx files parser"""
    def __init__(self, filename):
        """Xlsx (MS 2007 Excel) file parser class

        :param filename: xlsx filename for parsing
        """
        self.filename = filename

        self._zip_file = ZipFile(self.filename)
        self.workbook = load_workbook(filename=filename)
        self._tmp_path = filename[filename.rindex('/') + 1:] + '_tmp'

    def get_images(self):
        """ extracts information about used images in xlsx file

        :return: images data list of dicts with:

        .. code-block:: python

            {
                'id': image identifier,
                'pos': image position (row, column)
                'path': image path
                'descrp': image description
            }

        """
        zip_file = self._zip_file
        drawings = filter(lambda x: re.match(r'.*drawing\d+.xml$',
                                             x.filename),
                          zip_file.filelist)
        drawings_rel = filter(lambda x: re.match(r'.*drawing\d+.xml.rels',
                                                 x.filename),
                              zip_file.filelist)
        if not drawings:
                return []

        drawing = drawings[0]
        drawing_rel = drawings_rel[0]
        parser = etree.XMLParser(remove_blank_text=True)
        if not os.path.exists(self._tmp_path):
            os.mkdir(os.path.join(os.getcwdu(), self._tmp_path))
        data = []

        file_name = zip_file.extract(drawing, path=self._tmp_path)
        rel_file_name = zip_file.extract(drawing_rel, path=self._tmp_path)

        xml = etree.XML(open(file_name, 'r').read(), parser=parser)
        rel_xml = etree.XML(open(rel_file_name, 'r').read(),
                            parser=parser)
        position_nodes = xml.xpath('//xdr:from', namespaces=xml.nsmap)

        # parse image sources rel links (stored in separate file)
        image_sources = []
        for node in rel_xml.getchildren():
            image_sources.append(node.attrib)

        # build [row, column, image_id, image_path, image_name ] list
        # for images unpack
        # add [row, column]
        for node in position_nodes:
            column = node.xpath('./xdr:col',
                                namespaces=node.nsmap)[0].text
            row = node.xpath('./xdr:row',
                             namespaces=node.nsmap)[0].text
            data.append({
                'pos': (row, column)
            })
        name_nodes = xml.xpath('//a:blip', namespaces=xml.nsmap)

        for idx, node in enumerate(name_nodes):
            identifier = node.xpath('@r:embed',
                                    namespaces=node.nsmap)[0]
            identifier = identifier.replace('rId', '')
            path = 'xl/media/{image}'
            data[idx]['id'] = identifier

            source = filter(
                lambda x: re.match(
                    '.*image{id}\.\w+$'.format(id=identifier), x['Target']),
                image_sources
            )[0]
            target = source['Target']
            image_name = target[target.rindex('/') + 1:]
            data[idx]['path'] = path.format(image=image_name)
        image_detail_nodes = xml.xpath('//xdr:cNvPr',
                                       namespaces=xml.nsmap)
        # add [, image_desription]
        for idx, node in enumerate(image_detail_nodes):
            description = node.xpath('@descr')[0]
            data[idx]['descr'] = description

        # extract images
        for chunk in data:
            ident = chunk['id']
            file_blocks = filter(
                lambda x: re.match(r'.*image%s\.\w+$' % ident, x .filename),
                zip_file.filelist
            )
            for file_block in file_blocks:
                zip_file.extract(file_block, path=self._tmp_path)

        return data

    def get_data(self, sheet_name='Sheet1', fmt='std', sheet_range=None):
        """parse xlsx file and return dict data for it

        :param sheet_name: sheet title in xlsx workbook, Sheet1 by default
        :param fmt: output format, python dict by default,
            could be: json
        :param sheet_range: range getter cells, for example A1:C5

        :return: data map
        """

        worksheet = self.workbook.get_sheet_by_name(sheet_name)
        columns = worksheet.columns
        if sheet_range:
            columns = worksheet.range(sheet_range)

        cols = len(columns)
        rows = len(columns[0])
        data = {
            'rows': {},
        }
        if sheet_range:
            cells = columns
            for row in cells:
                json_row = []
                for cell in row:
                    json_row.append(cell.value)
                data['rows'][str(row)] = json_row
        else:
            # by default it stores contra versa to range columns
            for row in range(rows):
                json_row = []
                for col in range(cols):
                    json_row.append(columns[col][row].value)
                data['rows'][str(row)] = json_row

        if fmt in ('application/json', 'json'):
            return json.dumps(data, default=encoder)
        return data
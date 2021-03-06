# -*- coding: utf-8 -*-
"""
Test classes for parsing protein interaction files.

Author:  Greg Taylor (greg.k.taylor@gmail.com)
"""
import os
import unittest
import tempfile

from hub.dataload.sources.ConsensusPathDB.parser import CPDParser
from hub.dataload.sources.biogrid.parser import BiogridParser


class TestParserMethods(unittest.TestCase):
    """
    Test class for ConsensusPathDB parser functions.  The static methods are called on an actual
    dataset.
    """

    ConsensusPathDBFile = os.path.join(os.path.dirname(__file__), 'test_data/ConsensusPathDB_human_PPI')

    def test_CPD_parse(self):
        """
        Parse a test CPD file of 1000 lines, gather statistics, and assess results
        :return:
        """
        # Write the contents of the test ConsenesusPathDB file to a temporary file object
        test_file = open(TestParserMethods.ConsensusPathDBFile, mode="r")
        cpd = []
        for record in CPDParser.parse_cpd_tsv_file(test_file):
            cpd.append(record)

        ########################################################
        # Gather some useful statistics of the resulting dataset
        ########################################################
        # Sum total of interaction confidence
        self.assertGreater(self._total(cpd, 'interaction_confidence'), 305)

        # Average number of interact_participants
        self.assertGreater(self._list_average(cpd, 'interaction_participants'), 2.2)
        # Average number of interaction_publications
        self.assertGreater(self._list_average(cpd, 'interaction_publications'), 1.4)
        # Average number of source_databases
        self.assertGreater(self._list_average(cpd, 'source_databases'), 1.4)

        n = self._none_count(cpd)
        self.assertEqual(n['source_databases'], 0)
        self.assertLess(n['interaction_publications'], 2800)
        self.assertEqual(n['interaction_participants'], 0)
        self.assertLess(n['interaction_confidence'], 19000)

    def _num_values(self, records, field):
        """
        Compute the total number of non NoneType values for a field in a given record.
        :param records:
        :param field:
        :return:
        """
        # Number of records with non-null values
        total = 0
        for _r in records:
            if _r[field]:
                total = total + 1
        return total

    def _total(self, cpd, field):
        """
        Compute the sum total over the test dataset for a given record field.
        :param cpd:
        :param field:
        :return:
        """
        # Number of records with non-null values
        total = 0
        for _c in cpd:
            if _c[field]:
                total = total + _c[field]
        return total

    def _list_count(self, cpd, field):
        """
        Compute the count of list elements over the test dataset for a given record field.
        :param cpd:
        :param field:
        :return:
        """
        count = 0
        for _c in cpd:
            if _c[field]:
                count = count + len(_c[field])
        return count

    def _list_average(self, cpd, field):
        """
        Compute the average number of list elements over the test dataset for a given record field.
        :param cpd:
        :param field:
        :return:
        """
        count = self._list_count(cpd, field)
        return count / len(cpd)

    def _record_average(self, records, field1, field2):
        """
        Compute the average number of list elements over the test dataset for a given record field.
        :param cpd:
        :param field:
        :return:
        """
        count = 0
        for record in records:
            if record[field1][field2]:
                count = count + len(record[field1][field2])
        return count / len(records)

    def _find20(self, records, field):
        """

        :param records:
        :param field:
        :return:
        """
        i = 0
        for r in records:
            if r[field]:
                print("%s:%s" % (field, r[field]))
                i = i + 1
            if i >= 20:
                break

    def _none_count(self, records):
        """
        Count the number of NoneType occurences within the record set.
        :param records:
        :return:
        """

        # Data structure to return
        r = {}
        for field in records[0].keys():
            if isinstance(records[0][field], dict):
                r[field] = {}
                for subfield in records[0][field].keys():
                    r[field][subfield] = 0
            else:
                r[field] = 0

        # Calculate all none types - special case for dictionaries
        for record in records:
            for field in record.keys():
                if isinstance(record[field], dict):
                    for subfield in record[field].keys():
                        if not record[field][subfield]:
                            r[field][subfield] = r[field][subfield] + 1
                elif not record[field]:
                    r[field] = r[field] + 1

        return r

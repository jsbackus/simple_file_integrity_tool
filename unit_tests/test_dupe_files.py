from __future__ import unicode_literals

import os
import subprocess
import unittest
import datetime
import time

from brd_unit_base import BrdUnitBase

# Import brd in order to use some of its functions
# Note: we're expecting brd_unit_base to take care of path stuff
import brd

class TestDupeFiles(BrdUnitBase):
    """Unit tests for the dupe_files subcommand.
    """

    def setUp(self):
        # Call superclass's setup routine.
        super(TestDupeFiles,self).setUp()
        
    def tearDown(self):
        # Call superclass's cleanup routine
        super(TestDupeFiles,self).tearDown()

    def test_identical_trees(self):
        """Tests dupe_files subcommand with identical trees.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = \
            ['4 files with Fingerprint ' +
             '0x1a0372738bb5b4b8360b47c4504a27e6f4811493:',
             '    [rootA]/TreeA/DirA/LeafA/BunchOfAs.txt',
             '    [rootA]/LeafB/BunchOfAs.txt',
             '    [rootB]/TreeA/DirA/LeafA/BunchOfAs.txt',
             '    [rootB]/LeafB/BunchOfAs.txt',
             '4 files with Fingerprint ' +
             '0xfa75bf047f45891daee8f1fa4cd2bf58876770a5:',
             '    [rootA]/TreeA/DirA/LeafA/BunchOfBs.txt',
             '    [rootA]/LeafB/BunchOfBs.txt',
             '    [rootB]/TreeA/DirA/LeafA/BunchOfBs.txt',
             '    [rootB]/LeafB/BunchOfBs.txt',
             '2 files with Fingerprint ' +
             '0xff3785f53b503b7adb7e7a3b9eeef255eac0e276:',
             '    [rootA]/BunchOfCs.txt',
             '    [rootB]/BunchOfCs.txt', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_2( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Check targets
        scr_out = subprocess.check_output([self.script_name, 'dupe_files'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )
        
    def test_single_tree_with_duplicates(self):
        """Tests dupe_files subcommand with a single tree that has duplicate
        files.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = \
            ['2 files with Fingerprint ' +
             '0x1a0372738bb5b4b8360b47c4504a27e6f4811493:',
             '    [rootA]/TreeA/DirA/LeafA/BunchOfAs.txt',
             '    [rootA]/LeafB/BunchOfAs.txt',
             '2 files with Fingerprint ' +
             '0xfa75bf047f45891daee8f1fa4cd2bf58876770a5:',
             '    [rootA]/TreeA/DirA/LeafA/BunchOfBs.txt',
             '    [rootA]/LeafB/BunchOfBs.txt', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Check targets
        scr_out = subprocess.check_output([self.script_name, 'dupe_files'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )
        
    def test_output_option(self):
        """Tests dupe_files subcommand with --output option.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        out_file = 'test_output.txt'
        exp_out = \
            ['2 files with Fingerprint ' +
             '0x1a0372738bb5b4b8360b47c4504a27e6f4811493:\n',
             '    [rootA]/TreeA/DirA/LeafA/BunchOfAs.txt\n',
             '    [rootA]/LeafB/BunchOfAs.txt\n',
             '2 files with Fingerprint ' +
             '0xfa75bf047f45891daee8f1fa4cd2bf58876770a5:\n',
             '    [rootA]/TreeA/DirA/LeafA/BunchOfBs.txt\n',
             '    [rootA]/LeafB/BunchOfBs.txt\n']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Check --output
        scr_out = subprocess.check_output([self.script_name, 'dupe_files', 
                                           '--output', out_file], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        with open(out_file, 'rt') as f:
            scr_lines = f.readlines()

        # Verify results
        self.assertEqual( scr_out, '' )

        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

        # Remove output file and try again with -o option
        os.unlink( out_file )

        # Check -o
        scr_out = subprocess.check_output([self.script_name, 'dupe_files', 
                                           '-o', out_file], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        with open(out_file, 'rt') as f:
            scr_lines = f.readlines()

        # Verify results
        self.assertEqual( scr_out, '' )

        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

        # Clean up
        os.unlink( out_file )
        
    # def test_identical_files(self):
    #     """Tests dupe_files subcommand with identical files.
    #     """

    #     mod_time = int(time.time())
    #     check_time = datetime.datetime.fromtimestamp(mod_time)
    #     exp_out = ''

    #     # Call open_db, which should create db and its tables
    #     self.open_db( self.default_db, False )

    #     # Populate the database with schema 1.
    #     exp_data = self.get_schema_1( str(mod_time), check_time )
    #     self.populate_db_from_tree( exp_data )
    #     self.conn.close()

    #     # Dupe_Files targets
    #     scr_out = subprocess.check_output([self.script_name, 'dupe_files', 
    #                                        'rootA/TreeA/DirA/LeafA/BunchOfAs.txt', 
    #                                        'rootA/LeafB/BunchOfAs.txt'], 
    #                                       stderr=subprocess.STDOUT,
    #                                       universal_newlines=True)

    #     # Verify results
    #     self.assertEqual( scr_out, exp_out )

    # def test_file_vs_dir(self):
    #     """Tests dupe_files subcommand with file and directory.
    #     """

    #     mod_time = int(time.time())
    #     check_time = datetime.datetime.fromtimestamp(mod_time)
    #     exp_out = 'rootA/TreeA/DirA/LeafA/BunchOfAs.txt is a file.\n' + \
    #         'rootA/LeafB is a directory.\n'

    #     # Call open_db, which should create db and its tables
    #     self.open_db( self.default_db, False )

    #     # Populate the database with schema 1.
    #     exp_data = self.get_schema_1( str(mod_time), check_time )
    #     self.populate_db_from_tree( exp_data )
    #     self.conn.close()

    #     # Dupe_Files targets
    #     scr_out = subprocess.check_output([self.script_name, 'dupe_files', 
    #                                        'rootA/TreeA/DirA/LeafA/BunchOfAs.txt', 
    #                                        'rootA/LeafB'], 
    #                                       stderr=subprocess.STDOUT,
    #                                       universal_newlines=True)

    #     # Verify results
    #     self.assertEqual( scr_out, exp_out )
        
    # def test_dissimilar_trees(self):
    #     """Tests dupe_files subcommand with two dissimilar trees.
    #     """

    #     mod_time = int(time.time())
    #     check_time = datetime.datetime.fromtimestamp(mod_time)
    #     exp_out = ['Only in rootA/LeafB: BunchOfAs.txt',
    #                'Only in rootA/LeafB: BunchOfBs.txt',
    #                'Only in rootA/TreeA: DirA', '']

    #     # Call open_db, which should create db and its tables
    #     self.open_db( self.default_db, False )

    #     # Populate the database with schema 1.
    #     exp_data = self.get_schema_1( str(mod_time), check_time )
    #     self.populate_db_from_tree( exp_data )
    #     self.conn.close()

    #     # Dupe_Files targets
    #     scr_out = subprocess.check_output([self.script_name, 'dupe_files', 
    #                                        'rootA/TreeA', 'rootA/LeafB'], 
    #                                       stderr=subprocess.STDOUT,
    #                                       universal_newlines=True)
    #     scr_lines = scr_out.split('\n')

    #     # Verify results
    #     self.assertEqual( len(scr_lines), len(exp_out) )
    #     for exp_line in exp_out:
    #         self.assertTrue( exp_line in scr_lines )
        
# Allow unit test to run on its own
if __name__ == '__main__':
    unittest.main()

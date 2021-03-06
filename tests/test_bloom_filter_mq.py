#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2013 Qin Xuye <qin@qinxuye.me>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on 2013-6-1

@author: Chine
'''

import unittest
import tempfile
import shutil
import os

from cola.core.mq.store import Store
from cola.core.dedup import FileBloomFilterDeduper

class Test(unittest.TestCase):


    def setUp(self):
        self.dir_ = tempfile.mkdtemp()
        self.node_dir = os.path.join(self.dir_, 'node')
        deduper =  FileBloomFilterDeduper(
            os.path.join(self.dir_, 'bloomfilter'), 10
        )
        self.store = Store(self.node_dir, deduper=deduper,
                          mkdirs=True)

    def tearDown(self):
        self.store.shutdown()
        shutil.rmtree(self.dir_)
          
    def testPutGet(self):
        num = str(12345)
        
        self.assertEqual(self.store.put(num), num)
        self.assertEqual(self.store.put(num), None)
        
        num2 = str(67890)
        nums = [num, num2]
        self.assertEqual(self.store.put(nums), [num2])
        
        self.store.shutdown()
        self.store.deduper.shutdown()
        self.assertGreater(os.path.getsize(os.path.join(self.dir_, 'bloomfilter')), 0)
        
        bloom_filter_deduper = FileBloomFilterDeduper(
            os.path.join(self.dir_, 'bloomfilter'), 5
        )
        self.store = Store(self.node_dir, deduper=bloom_filter_deduper)
        
        num3 = str(13579)
        nums = [num, num2, num3]
        self.assertEqual(self.store.put(nums), [num3])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
try:
 from validate_index import validate_records
except ImportError:
 validate_records=None
class IndexContract(unittest.TestCase):
 def test_good_record_and_bad_classification(self):
  self.assertIsNotNone(validate_records,'index validation not implemented')
  row={'id':'x','title':'文章','publisher':'作者','published_date':None,'date_note':'unknown','url':'https://example.com/x','read_status':'title_only','primary_category':'数据研发','tags':[],'summary':'待阅读'}
  self.assertEqual(validate_records([row]),[])
  bad=dict(row,primary_category='other')
  self.assertTrue(validate_records([bad]))
 def test_duplicate_and_missing_fields(self):
  self.assertIsNotNone(validate_records,'index validation not implemented')
  self.assertTrue(validate_records([{}]))
  row={'id':'x','title':'a','publisher':'b','published_date':'2026-11-01','url':'https://example.com/x','read_status':'read','primary_category':'数据agent','tags':[],'summary':'a','reading_evidence':'正文已读'}
  self.assertTrue(validate_records([row,row]))
  del row['reading_evidence']
  self.assertTrue(validate_records([row]))

import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
try:
 from audit_coverage import audit
except ImportError:
 audit=None

class CoverageAudit(unittest.TestCase):
 def fixture(self):
  account={'id':'a','name':'账号','identity_verified':True,'identity_evidence':'official profile record','history_source':'official_history','history_evidence':['page1','boundary-page'],'history_complete':True,'lower_boundary_checked':True,'cutoff_checked':True,'pushes':[{'id':'p','published_date':'2026-01-01','item_count':1,'evidence':'push-page'}]}
  article={'id':'m1','account_id':'a','push_id':'p','position':1,'published_date':'2026-01-01','title':'文章','url':'https://mp.weixin.qq.com/s/example','read_status':'read','reading_evidence':['正文段落定位'],'visuals_checked':True,'version_checked_at':'2026-11-01'}
  return [account],[article]
 def test_unknown_total_is_not_zero_or_complete(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  a,m=self.fixture();a[0]['history_complete']=False
  report=audit(a,[],expected_accounts=1)
  self.assertFalse(report['all_complete']);self.assertIsNone(report['accounts'][0]['expected_articles'])
 def test_full_read_requires_closed_inventory(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  a,m=self.fixture();r=audit(a,m,expected_accounts=1)
  self.assertTrue(r['all_complete']);self.assertEqual(r['accounts'][0]['full_read'],1)
 def test_missing_secondary_article_blocks(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  a,m=self.fixture();a[0]['pushes'][0]['item_count']=2
  self.assertFalse(audit(a,m,expected_accounts=1)['all_complete'])
 def test_partial_visuals_and_deleted_articles_block(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  for field,value in [('visuals_checked',False),('read_status','deleted'),('reading_evidence',[])]:
   a,m=self.fixture();m[0][field]=value
   self.assertFalse(audit(a,m,expected_accounts=1)['all_complete'])
 def test_duplicate_or_outside_window_cannot_pass(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  a,m=self.fixture()
  for rows in [m+m,[dict(m[0],published_date='2025-10-31')],[dict(m[0],position=2)]]:
   self.assertFalse(audit(a,rows,expected_accounts=1)['all_complete'])
 def test_search_snippets_and_unverified_identity_block(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  for field,value in [('history_source','web_search'),('identity_verified',False),('lower_boundary_checked',False),('history_evidence',[])]:
   a,m=self.fixture();a[0][field]=value
   self.assertFalse(audit(a,m,expected_accounts=1)['all_complete'])
 def test_unknown_account_and_mismatched_push_date_block(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  a,m=self.fixture()
  for rows in [[dict(m[0],account_id='unknown')],[dict(m[0],published_date='2026-02-01')]]:
   self.assertFalse(audit(a,rows,expected_accounts=1)['all_complete'])
 def test_missing_article_id_and_bad_push_count_block_without_crash(self):
  self.assertIsNotNone(audit,'coverage auditor missing')
  a,m=self.fixture();m[0]['id']=''
  self.assertFalse(audit(a,m,expected_accounts=1)['all_complete'])
  a,m=self.fixture();a[0]['pushes'][0]['item_count']='1'
  self.assertFalse(audit(a,m,expected_accounts=1)['all_complete'])

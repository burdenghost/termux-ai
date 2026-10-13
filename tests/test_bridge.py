import pathlib,tempfile,unittest
from bridge.common import safe_path
class Paths(unittest.TestCase):
 def test_inside(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d).resolve(); (root/"a").write_text("ok"); self.assertEqual(safe_path(root,"a"),root/"a")
 def test_traversal(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError): safe_path(pathlib.Path(d).resolve(),"../outside")
 def test_absolute(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError): safe_path(pathlib.Path(d).resolve(),"/etc/passwd")
if __name__=="__main__": unittest.main()

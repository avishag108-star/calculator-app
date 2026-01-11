import os

def test_app_file_exists():
  
    assert os.path.exists('app.py')

def test_simple_logic():
   
    assert 1 + 1 == 2

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from app import app

class TestPacificAtlanticE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.server_thread = Thread(target=cls.app.run, kwargs={'debug': False, 'use_reloader': False})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server_thread.join()

    def setUp(self):
        self.driver.get('http://127.0.0.1:5000')

    def test_empty_matrix(self):
        """Test with an empty matrix"""
        matrix_input = '[]'
        expected_output = ('[]')
        self._run_test_case(matrix_input, expected_output)

    def test_single_cell(self):
        """Test with a single cell matrix"""
        matrix_input = '[[1]]'
        expected_output = '[[0,0]]'
        self._run_test_case(matrix_input, expected_output)

    def test_single_row(self):
        """Test with a single row matrix"""
        matrix_input = '[[1,2,2,3,5]]'
        expected_output = '[[0,0],[0,1],[0,2],[0,3],[0,4]]'
        self._run_test_case(matrix_input, expected_output)

    def test_single_column(self):
        """Test with a single column matrix"""
        matrix_input = '[[1],[2],[2],[3],[5]]'
        expected_output = '[[0,0],[1,0],[2,0],[3,0],[4,0]]'
        self._run_test_case(matrix_input, expected_output)

    def test_increasing_heights(self):
        """Test with a matrix where heights are strictly increasing"""
        matrix_input = '[[1,2,3],[4,5,6],[7,8,9]]'
        expected_output = '[[0,2],[1,2],[2,0],[2,1],[2,2]]'
        self._run_test_case(matrix_input, expected_output)

    def test_decreasing_heights(self):
        """Test with a matrix where heights are strictly decreasing"""
        matrix_input = '[[9,8,7],[6,5,4],[3,2,1]]'
        expected_output = '[[0,0],[0,1],[0,2],[1,0],[2,0]]'
        self._run_test_case(matrix_input, expected_output)

    def test_equal_heights(self):
        """Test with a matrix where all heights are the same"""
        matrix_input = '[[1,1,1],[1,1,1],[1,1,1]]'
        expected_output = '[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]'
        self._run_test_case(matrix_input, expected_output)

    def test_large_matrix(self):
        """Test with a large matrix to ensure performance"""
        matrix_input = '[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]'
        expected_output = '[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]'
        self._run_test_case(matrix_input, expected_output)

    def test_all_cells_flow(self):
        """Test with a matrix where all cells can flow to both oceans"""
        matrix_input = '[[1,1,1],[1,1,1],[1,1,1]]'
        expected_output = '[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]'
        self._run_test_case(matrix_input, expected_output)

    def test_no_cells_flow(self):
        """Test with a matrix where no cells can flow to both oceans"""
        matrix_input = '[[10,10,10],[10,1,10],[10,10,10]]'
        expected_output = '[[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[2,2]]'
        self._run_test_case(matrix_input, expected_output)

    def test_diagonal_increasing(self):
        """Test with a matrix where heights increase diagonally"""
        matrix_input = '[[1,2,3],[2,3,4],[3,4,5]]'
        expected_output = '[[0,2],[1,2],[2,0],[2,1],[2,2]]'
        self._run_test_case(matrix_input, expected_output)

    def test_diagonal_decreasing(self):
        """Test with a matrix where heights decrease diagonally"""
        matrix_input = '[[5,4,3],[4,3,2],[3,2,1]]'
        expected_output = '[[0,0],[0,1],[0,2],[1,0],[2,0]]'
        self._run_test_case(matrix_input, expected_output)

    def test_checkerboard_pattern(self):
        """Test with a checkerboard pattern matrix"""
        matrix_input = '[[1,2,1],[2,1,2],[1,2,1]]'
        expected_output = '[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]]'
        self._run_test_case(matrix_input, expected_output)

    def test_ridges_and_valleys(self):
        """Test with a matrix that has ridges and valleys"""
        matrix_input = '[[1,3,1,3,1],[2,1,2,1,2],[1,3,1,3,1],[2,1,2,1,2],[1,3,1,3,1]]'
        expected_output = '[[0,3],[0,4],[1,4],[3,0],[4,0],[4,1]]'
        self._run_test_case(matrix_input, expected_output)

    def test_single_ocean_reachable(self):
        """Test with a matrix where cells can only flow to one ocean"""
        matrix_input = '[[5,5,5,5],[5,1,1,5],[5,1,1,5],[5,5,5,5]]'
        expected_output = '[[0,0],[0,1],[0,2],[0,3],[1,0],[1,3],[2,0],[2,3],[3,0],[3,1],[3,2],[3,3]]'
        self._run_test_case(matrix_input, expected_output)

    def test_matrix_with_barriers(self):
        """Test with a matrix where some cells act as barriers"""
        matrix_input = '[[1,2,3,4],[2,3,1,5],[3,1,2,6],[4,5,6,7]]'
        expected_output = '[[0,3],[1,3],[2,3],[3,0],[3,1],[3,2],[3,3]]'
        self._run_test_case(matrix_input, expected_output)

    def _run_test_case(self, matrix_input, expected_output):
        matrix_input_element = self.driver.find_element(By.ID, 'matrixInput')
        matrix_input_element.clear()
        matrix_input_element.send_keys(matrix_input)
        self.driver.find_element(By.TAG_NAME, 'button').click()
        time.sleep(1)
        result = self.driver.find_element(By.ID, 'result').text
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

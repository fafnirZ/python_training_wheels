
import pytest
from edm.main import point_distance, point_distance_manual
from hypothesis import given
import hypothesis.strategies as st
import numpy as np

# Define a strategy for generating n x 2 matrices
# USING INTEGERS, floats are annoying
def random_n_by_2_matrix():
  MAX_Y = 1000000
  MAX_X = 2
  return st.lists(st.lists(st.integers(min_value=-100, max_value=100), min_size=MAX_X, max_size=MAX_X),
                  min_size=1, max_size=MAX_Y).map(np.array)



@pytest.mark.parametrize("num_trials", [5,10,100])
@given(matrix=random_n_by_2_matrix())
def test_equality(num_trials, matrix, benchmark):
  for _ in range(num_trials):
    res_manual = point_distance_manual(matrix)
    res_edm = point_distance(matrix)
    # assert (res_edm==res_manual).all()
    assert np.allclose(res_edm, res_manual) # allows for floating point errors 

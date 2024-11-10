
from pathlib import Path
import time
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
def test_equality(num_trials, matrix):
  for _ in range(num_trials):
    res_manual = point_distance_manual(matrix)
    res_edm = point_distance(matrix)
    # assert (res_edm==res_manual).all()
    assert np.allclose(res_edm, res_manual) # allows for floating point errors 



@pytest.mark.parametrize("num_trials", [500])
@given(matrix=random_n_by_2_matrix())
def test_benchmark(num_trials, matrix):
  avg_manual = 0
  avg_edm = 0
  for _ in range(num_trials):
    time_s = time.time()
    res_manual = point_distance_manual(matrix)
    time_e = time.time()
    avg_manual += (time_e - time_s)

    time_s = time.time()
    res_edm = point_distance(matrix)
    time_e = time.time()
    avg_edm += (time_e - time_s)
    # assert (res_edm==res_manual).all()
    assert np.allclose(res_edm, res_manual) # allows for floating point errors 

  avg_manual /= num_trials
  avg_edm /= num_trials

  with (Path.cwd() / "benchmark.txt").open("a") as f:
    f.write(f"num_trials: {num_trials}\n")
    f.write(f"avg_manual: {avg_manual}\n")
    f.write(f"avg_edm: {avg_edm}\n")
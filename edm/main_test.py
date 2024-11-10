
import pytest
from edm.main import point_distance, point_distance_manual
from hypothesis import given
import hypothesis.strategies as st
import numpy as np

# Define a strategy for generating n x 2 matrices
def random_n_by_2_matrix():
  MAX_Y = 1000000
  MAX_X = 2
  return st.lists(st.lists(st.floats(min_value=-100, max_value=100), min_size=MAX_X, max_size=MAX_X),
                  min_size=1, max_size=MAX_Y).map(np.array)


def generate_n_cases(n):
  strategy = random_n_by_2_matrix()
  return [
    strategy.example()
    for _ in range(n)
  ]


@pytest.mark.parametrize(
  "case",
  [
    *generate_n_cases(100)
  ]
)
def test_equality(case):
  res_manual = point_distance_manual(case)
  res_edm = point_distance(case)

  # assert (res_edm==res_manual).all()
  assert np.allclose(res_edm, res_manual) # allows for floating point errors 
import pytest
import os
import sys
from io import StringIO

from src.island_hopper import read_input, parse_input, find_itinerary

# data
file_input1 = os.path.join(os.path.dirname(__file__), 'examples', 'input1')
file_input2 = os.path.join(os.path.dirname(__file__), 'examples', 'input2')
raw_input1 = ['6', '4', '0 by-sea, 2 by-sea, 3 by-sea', '0 by-sea, 5 airborne', '0 airborne, 5 by-sea', '2 airborne']
raw_input2 = ['2', '3', '0 by-sea', '0 airborne', '1 by-sea']
num_hops1, num_customers1, requirements1 = 6, 4, [{0: 'by-sea', 2: 'by-sea', 3: 'by-sea'}, {0: 'by-sea', 5: 'airborne'}, {0: 'airborne', 5: 'by-sea'}, {2: 'airborne'}]
num_hops2, num_customers2, requirements2 = 2, 3, [{0: 'by-sea'}, {0: 'airborne'}, {1: 'by-sea'}]
output1 = "0 by-sea, 1 by-sea, 2 airborne, 3 by-sea, 4 by-sea, 5 by-sea"
output2="NO ITINERARY"

# tests
def test_read_input_file():
    """
    Test read_input function with file
    """
    result = read_input(file_input1)
    assert result == raw_input1

def test_read_input_stdin(monkeypatch):
    """
    Test read_input function with stdin
    """
    with open(file_input2, 'r') as f:
        test_input = f.read()
    monkeypatch.setattr(sys, 'stdin', StringIO(test_input))
    result = read_input()
    assert result == raw_input2

@pytest.mark.parametrize("input_value, expected", [
    (raw_input1, (num_hops1, num_customers1, requirements1)),
    (raw_input2, (num_hops2, num_customers2, requirements2))
    ])

def test_parse_input(input_value, expected):
    """
    Test parse_input function
    """
    assert parse_input(input_value) == expected

@pytest.mark.parametrize("input_value, expected", [
    ((num_hops1, requirements1), output1),
    ((num_hops2, requirements2), output2)
    ])

def test_find_itinerary(input_value, expected):
    """
    Test find_itinerary function
    """
    assert find_itinerary(*input_value) == expected

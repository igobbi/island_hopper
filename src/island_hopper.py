import sys
from ortools.sat.python import cp_model


def read_input(file=None):
    """
    Read input from stdin or file

    If the file name is provided, it reads from file,
    otherwise it reads from stdin (default)

    Parameters:
    file (str, optional): path to input file (default: None)

    Returns:
    list: list of lines read from input

    Raises:
    FileNotFoundError: when the specified file does not exist.
    Exception: when there is an error reading the file
    """
    try:
        if file:
            with open(file, 'r') as f:
                data = f.read().strip()
        else:
            data = sys.stdin.read().strip()
        return data.split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def parse_input(data):
    """
    Parse input data into number of hops, number of customers and
    list of requirements for all customers

    The first line contains the number of hops (H),
    the second the number of customers (C),
    the following lines contain the requirements of all customers

    Parameters:
    data (list of str): the first element is the number of hops (H),
                        the second element is the number of customers (C),
                        and the following elements are strings representing
                        customer requirements formatted as 'h t', where 'h'
                        is an integer representing the hop and 't' a string,
                        either 'airborne' or 'by-sea'

    Returns:
    num_hops (int): number of hops
    num_customers (int): number of customers
    requirements_list (list of dict):
        list of dictionary h:t for each customer
    """
    num_hops = int(data[0])
    num_customers = int(data[1])
    requirements_list = []

    for line in data[2:]:
        requirements = line.split(', ')
        req_dict = {}
        for req in requirements:
            key, value = req.split()
            req_dict[int(key)] = value
        requirements_list.append(req_dict)
    return num_hops, num_customers, requirements_list


def find_itinerary(num_hops, requirements_list):
    """
    Find the optimal itinerary based on customer requirements

    A constrained programming model is built where the objective is
    to minimize the number of 'airborne' hops while satisfying customer
    constraints. For each customer, the coinstraint is that at least one
    of their transportation preferences is met.
    If no itinerary is possible, the function returns 'NO ITINERARY'
    constraint programming model to determine an

    Parameters:
    num_hops (int): number of hops (H)
    requirements_list (list of dict): list of customer transportation requirements.
                                       The format is h:t where h is the hop index
                                       and t is either 'airborne' or 'by-sea'

    Returns:
    str: a string representing the optimal itinerary in the format "h t".
         If no itinerary is possible, it returns "NO ITINERARY".

    Raises:
    RuntimeError: the solver completes with an unexpected status
    """
    # build model
    model = cp_model.CpModel()
    # variables
    hops = [model.new_bool_var(f"hop_{h}") for h in range(num_hops)]
    # constraints
    for requirements in requirements_list:
        constraints = []
        for h, t in requirements.items():
            if t == "airborne":
                constraints.append(hops[h])
            else:
                constraints.append(~hops[h])
        model.add_bool_or(constraints)

    # objective
    model.minimize(sum(hops))

    # solve
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # generate output string
    if status == cp_model.OPTIMAL:
        itinerary = []
        for h in range(num_hops):
            transport = "airborne" if solver.value(hops[h]) == 1 else "by-sea"
            itinerary.append(f"{h} {transport}")
        return ', '.join(itinerary)
    elif status == cp_model.INFEASIBLE:
        return "NO ITINERARY"
    else:
        raise RuntimeError(f"Solver failed with status: {status}.")

def main():
    file = None
    if len(sys.argv) > 1:
        file = sys.argv[1]

    data = read_input(file)
    num_hops, num_customers, requirements_list = parse_input(data)
    result = find_itinerary(num_hops, requirements_list)
    print(result)


if __name__ == "__main__":
    main()

from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model


def main():
    # This program tries to find an optimal assignment of workers to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each worker can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests.
    num_workers = 5
    num_shifts = 3
    workers_per_shift = [3, 2, 5]
    num_days = 7
    all_workers = range(num_workers)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    shift_requests = [[[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1],
                       [0, 1, 0], [0, 0, 1]],
                      [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],
                       [0, 0, 0], [0, 0, 1]],
                      [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],
                       [0, 1, 0], [0, 0, 0]],
                      [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],
                       [1, 0, 0], [0, 0, 0]],
                      [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],
                       [0, 1, 0], [0, 0, 0]]]
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: worker 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_workers:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d,
                                                                          s))

    # Each shift is assigned to exactly one worker in .
    for d in all_days:
        count = 0
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_workers) == workers_per_shift[count])
            count = count + 1

    # # Each worker works at most one shift per day.
    # for n in all_workers:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # # min_shifts_assigned is the largest integer such that every worker can be
    # # assigned at least that number of shifts.
    # min_shifts_per_worker = (num_shifts * num_days) // num_workers
    # max_shifts_per_worker = min_shifts_per_worker + 1
    # for n in all_workers:
    #     num_shifts_worked = sum(
    #         shifts[(n, d, s)] for d in all_days for s in all_shifts)
    #     model.Add(min_shifts_per_worker <= num_shifts_worked)
    #     model.Add(num_shifts_worked <= max_shifts_per_worker)

    model.Maximize(
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_workers
            for d in all_days for s in all_shifts))
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)
    for d in all_days:
        print('Day', d)
        for n in all_workers:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    if shift_requests[n][d][s] == 1:
                        print('Worker', n, 'works shift', s, '(requested).')
                    else:
                        print('Worker', n, 'works shift', s, '(not requested).')
        print()

    # Statistics.
    print()
    print('Statistics')
    # print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
    #       '(out of', num_workers * min_shifts_per_worker, ')')
    print('  - wall time       : %f s' % solver.WallTime())


if __name__ == '__main__':
    main()

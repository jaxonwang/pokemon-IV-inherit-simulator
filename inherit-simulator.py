import random
import itertools
import multiprocessing

CORES = 8
SAMPLE_SIZE = 1000000


def mating(father, mother):
    from_which_parent = ['f' if random.randint(
        0, 1) else 'm' for i in range(6)]
    choose_five = [True] * 6
    choose_five[random.randint(0, 5)] = False

    heredity_policy = zip(from_which_parent, choose_five)

    child = [0] * 6
    for i, (which_parent, choosen) in enumerate(heredity_policy):
        if choosen is False:
            child[i] = random.randint(0, 31)
        else:
            child[i] = father[i] if which_parent == "f" else mother[i]
    return child


def volumne_test(father, mother, IV_filter, sample_size):
    """
    return ther numbers of child who passes the filter under
    a test with the sample_size
    """
    count = 0
    for i in range(sample_size):
        child = mating(mother, father)
        if IV_filter(child):
            count += 1
    return count


def IV_to_child(father_IV_num=None, mother_IV_num=None,
                child_IV_needed=None,
                father=None, mother=None, childs=None, IV_filter=None):
    if father and mother and childs:
        IV_filter = lambda c: c in childs
    elif father_IV_num and mother_IV_num and child_IV_needed:
        assert(father_IV_num <= 6 and mother_IV_num <= 6)

        # default father IV and mother IV are complement to each other
        father = [31] * father_IV_num + [0] * (6 - father_IV_num)
        mother = [0] * (6 - mother_IV_num) + [31] * mother_IV_num
        IV_filter = lambda child: len(
            filter(lambda x: x == 31, child)) >= child_IV_needed
    elif father and mother and IV_filter:
        pass
    else:
        raise TypeError("wrong input")
    return volumne_test(father, mother, IV_filter, SAMPLE_SIZE)


def IV_filter_generator(child):
    """
    child = [-1,31,31,31,31,31] -1 for any
    """
    def _IV_filter(c):
        for i, v in enumerate(child):
            if v != -1 and c[i] != v:
                return False
        return True
    return _IV_filter


def f(x):
    return IV_to_child(**x)


def multiprocess_probability_test(**kv):
    p = multiprocessing.Pool(CORES)
    ret = p.map(f, [kv] * CORES)
    return float(sum(ret)) / SAMPLE_SIZE / CORES

if __name__ == "__main__":
    # print multiprocess_probability_test(IV_to_child, 5, 5, 6)
    print multiprocess_probability_test(father=[31, 31, 31, 31, 31, 31],
                                        mother=[31, 31, 31, 31, 31, 31],
                                        childs=[[31, 31, 31, 31, 31, 31], ])
    # perfect 5V and 6V
    print multiprocess_probability_test(father=[31, 0, 31, 31, 31, 31],
                                        mother=[31, 31, 31, 31, 31, 31],
                                        IV_filter=IV_filter_generator([31, -1, 31, 31, 31, 31]))
    # not perfect 5V and 6V
    print multiprocess_probability_test(father=[31, 31, 0, 31, 31, 31],
                                        mother=[31, 31, 31, 31, 31, 31],
                                        IV_filter=IV_filter_generator([31, -1, 31, 31, 31, 31]))

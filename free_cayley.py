import matplotlib.pyplot as plt
from itertools import chain

GENERATORS = {"a", "b", "a_inv", "b_inv"}
FIGSIZE = (15, 15)
MARKER_SIZE = 2
MAX_ORDER = 9
EXCLUDE = False
KNOT_FILTER = lambda braid: get_num_components(braid) == 1


def generate_braids(max_order, parent_braid=(), exclude_redundant=True):
    """
    Generate all possible braids of order 0 to max_order
    """
    if len(parent_braid) == max_order:
        return [parent_braid]

    redundant_op = None
    if parent_braid and exclude_redundant:
        prev_op = parent_braid[-1]
        redundant_op = prev_op[0] if prev_op.endswith("_inv") else prev_op + "_inv"

    braids = []
    for g in GENERATORS - {redundant_op}:
        new_braid = parent_braid + (g,)
        braids.extend(generate_braids(max_order, new_braid, exclude_redundant))
    return braids


def get_braid_pos(braid):
    """
    Get the positional embedding of a braid in the free group cayley graph
    """
    pos = [0, 0]
    for i, op in enumerate(braid):
        op_sign = -1 if op.endswith("_inv") else 1
        if op[0] == "a":
            pos[0] += op_sign * (1 / 2) ** i
        elif op[0] == "b":
            pos[1] += op_sign * (1 / 2) ** i
    return pos


def get_num_components(braid):
    """
    Get the number of connected components in the braid
    """
    perm = list(range(3))
    for op in braid:
        if op[0] == "a":
            perm[0], perm[1] = perm[1], perm[0]
        elif op[0] == "b":
            perm[1], perm[2] = perm[2], perm[1]
    mismatches = sum(perm[i] != i for i in range(3))
    return {0: 3, 2: 2, 3: 1}[mismatches]


if __name__ == "__main__":
    print("Generating braids...")
    braids = list(
        chain(
            *[generate_braids(i, exclude_redundant=EXCLUDE) for i in range(MAX_ORDER)]
        )
    )
    print(f"Generated {len(braids)} braids")

    if KNOT_FILTER:
        print("Filtering braids...")
        braids = [braid for braid in braids if KNOT_FILTER(braid)]
        print(f"Filtered to {len(braids)} braids")

    print("Computing braid positions...")
    braid_positions = [get_braid_pos(braid) for braid in braids]

    print("Computing number of components...")
    num_components = [get_num_components(braid) for braid in braids]

    print("Plotting...")
    plt.figure(figsize=FIGSIZE)
    plt.axis("equal")
    plt.axis("off")
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.scatter(
        [pos[0] for pos in braid_positions],
        [pos[1] for pos in braid_positions],
        c=num_components,
        cmap="Set1",
        s=MARKER_SIZE,
        marker="s",
    )
    plt.savefig("free_cayley.png")
    plt.show()

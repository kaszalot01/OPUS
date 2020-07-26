import sys
from collections import deque
from pathlib import Path

from opus.lang.parser import parser
from opus.lang.ir import System


def change_player(player: int) -> int:
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else:
        raise ValueError("Incorrect player number: " + str(player))


def prettify_suits(system_text: str) -> str:
    # TODO - this will replace capitals in comments. Change that.
    system_text = system_text.replace("C", "♣")
    system_text = system_text.replace("D", "♦")
    system_text = system_text.replace("H", "♥")
    system_text = system_text.replace("S", "♠")
    return system_text


def player_comment(player) -> str:
    return f"# player {player}"


def add_bid_comments(system_text: str, system: System) -> str:
    lines = system_text.split("\n")

    branch_list_queue = deque()
    branch_list_queue.append((system.branches, 1))

    while len(branch_list_queue) > 0:
        branch_list, current_player = branch_list_queue.popleft()

        for processed_branch in branch_list:

            branch_player = current_player
            for bid in processed_branch.bids:
                print(bid.meta, branch_player)
                line_index = bid.meta.line - 1  # line numbers are indexed form 0
                new_line = lines[line_index] + "  " + player_comment(branch_player)
                lines[line_index] = new_line
                branch_player = change_player(branch_player)

            branch_list_queue.append((processed_branch.children, branch_player))

    return "\n".join(lines)


def prettify(system_text: str, suits=True, bids=True) -> str:

    system = System.parse_system(system_text)

    pretty_text = system_text
    if suits:
        pretty_text = prettify_suits(pretty_text)
    if bids:
        pretty_text = add_bid_comments(pretty_text, system)

    system_from_pretty = System.parse_system(pretty_text)
    assert system_from_pretty == system
    return pretty_text


def main():
    fname = sys.argv[1]
    path = Path(fname)

    with open(path) as file:
        system_text = file.read()

    pretty_text = prettify(system_text, False)

    new_path = path.parent / (path.stem + "_pretty" + path.suffix)
    with open(new_path, "w") as file:
        file.write(pretty_text)


if __name__ == '__main__':
    main()

import os.path
from typing import List


def extract_paths(drop_event_data: str) -> List[str]:
    # the syntax is horrible

    remaining_data = drop_event_data

    result = []

    while len(remaining_data) > 0:

        remaining_data = remaining_data.strip(" ")

        # Syntax:
        # if path does not contain any spaces/special characters:
        #   path is not encased in anything --> can simply read to next space
        # if path does contain spaces or special characters:
        #   if there are equally many { as } in the path:
        #      path is contained within {}
        #      { and } inside the path are not escaped
        #   if more } than { are inside the path:
        #      path is not contained within {} but all spaces and { and } are escaped with \\
        #   if more { than } are inside the path:
        #      path is not contained within {} but all spaces and { and } are escaped with \\

        # Example:
        # 'D:/image\\ 1\\{.webp {D:/image 1{ }.webp} {D:/image 1{ } .webp} D:/image\\ 1\\}.webp D:/image\\ 1\\}\\ .webp'

        if len(remaining_data) == 0:
            break

        if remaining_data.startswith("{"):

            close_on_next_space = False
            opens = 0

            for pos in range(0, len(remaining_data)):

                if pos == len(remaining_data) - 1:
                    result.append(remaining_data[1:-1])
                    remaining_data = ""
                    break

                if remaining_data[pos] == "{":
                    opens += 1

                elif remaining_data[pos] == "}":
                    opens -= 1
                    close_on_next_space = opens == 0

                elif remaining_data[pos] == " " and close_on_next_space:
                    result.append(remaining_data[1:pos - 1])
                    remaining_data = remaining_data[pos + 1:]
                    break

                else:
                    close_on_next_space = False
        else:

            for pos in range(0, len(remaining_data)):

                if remaining_data[pos] == " ":

                    if pos > 0 \
                            and remaining_data[pos - 1] == "\\":
                        continue
                    else:
                        next_path = remaining_data[0:pos]
                        next_path = next_path.replace("\\", "")  # remove escapes
                        result.append(next_path)
                        remaining_data = remaining_data[pos + 1:]
                        break
                elif pos == len(remaining_data) - 1:
                    next_path = remaining_data
                    next_path = next_path.replace("\\", "")  # remove escapes
                    result.append(next_path)
                    remaining_data = ""

    return [os.path.realpath(path) for path in result]

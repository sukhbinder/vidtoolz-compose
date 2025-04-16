import vidtoolz
import subprocess
import os
import shlex
import argparse

EXAMPLE_TEXT = """
Input file which contains the composition of the videos.

Example file content

# continous, howmany=3,audfile="/Users/sukhbindersingh/Downloads/Har Har Shambhu-(Mr-Jat.in).mp3",prefix=kotilingestwar
IMG_2494.MOV
IMG_9122.MOV
IMG_9123.MOV
# mconcat
IMG_2585.MOV
# continous, howmany=4,audio=19FLOOR,prefix=Markendeshwar
IMG_7476.MOV
IMG_7520.MOV
IMG_7552.MOV
# continous, howmany=5,audfile="/Users/sukhbindersingh/Downloads/Be Humble.mp3",prefix=Markendeshwar,startat=30
IMG_2664.MOV
IMG_2665.MOV
"""


# def main():
#     parser = argparse.ArgumentParser(
#         description=, formatter_class=argparse.RawTextHelpFormatter
#     )
#     parser.add_argument("input", help="See example")
#     parser.add_argument("-d","--debug", action="store_true", help="Will create all the files but will not run the cmds")
#     parser.add_argument("-v","--valid", action="store_true", help="Will validate the cmds")
#     args = parser.parse_args()
#     compose_video(args.input, args.debug, args.valid)


def compose_video(fname, debug=False, valid=False):
    """Compose Videos using the supplied compose_vid file"""

    # Parse the file
    with open(fname, "r") as fin:
        lines = fin.readlines()

    lnos = [i for i, line in enumerate(lines) if line.startswith("#")]
    lnos.append(len(lines))

    fpath = os.path.dirname(fname)

    # Generate the files and necessarry command
    commands = []
    for i, l in enumerate(lnos[:-1]):
        file = os.path.join(fpath, f"file_{i}.txt")
        cmdline = lines[l].strip().replace("#", "").replace("=", " ").split(",")
        cmdline = (
            [cmdline[0].strip()] + [file] + ["--" + cmd.strip() for cmd in cmdline[1:]]
        )
        cmdstr = " ".join(cmdline)
        cmdline2 = shlex.split(cmdstr)
        commands.append(cmdline2)
        # sellines = lines[l:lnos[i+1]]
        with open(file, "w") as fout:
            sellines = lines[l + 1 : lnos[i + 1]]
            sellines[-1] = sellines[-1].strip()
            fout.writelines(sellines)

    with open(os.path.join(fpath, "cmds.txt"), "w") as fout:
        for cmd in commands:
            fout.write(" ".join(cmd) + "\n")

    # Run all commands in sequence
    failed = []
    for cmd in commands:
        print(cmd)
        if not debug and not valid:
            try:
                iret = subprocess.call(cmd)
            except Exception as ex:
                failed.append(cmd)
        else:
            _ = check_cmd(cmd)

    print("FAILED CMD")
    print("###" * 10)
    print("###" * 10)
    for i in failed:
        print(i)
    print("###" * 10)
    print("###" * 10)


def check_cmd(command):
    try:
        # Run the command using subprocess and capture the output
        subprocess.check_output(command + ["--help"], shell=True)
    except subprocess.CalledProcessError as e:
        # If there's an error, report it to the user
        print(f"Error running command '{command}' ")


def create_parser(subparser):
    parser = subparser.add_parser("compose", description="Compose Videos using the supplied compose_vid file", 
                                   formatter_class=argparse.RawTextHelpFormatter)
    # Add subprser arguments here.
    parser.add_argument("input", help=EXAMPLE_TEXT)
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Will create all the files but will not run the cmds",
    )
    parser.add_argument(
        "-v", "--valid", action="store_true", help="Will validate the cmds"
    )
    return parser


class ViztoolzPlugin:
    """Compose video"""

    __name__ = "compose"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # add actual call here
        compose_video(args.input, args.debug, args.valid)

    def hello(self, args):
        # this routine will be called when "vidtoolz "compose is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


compose_plugin = ViztoolzPlugin()

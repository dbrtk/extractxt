
import shlex
import subprocess


def run_command(cmd: str = None) -> str:
    """ Runs the provided shell command and  returns the stdout.

    :param cmd:
    :return:
    """
    result = subprocess.run(
        shlex.split(cmd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def get_encoding(path: str = None):
    """ Returns file's encoding.

    :param path:
    :return:
    """
    return run_command("file -b --mime-encoding %s" % path)


def get_mimetype(path: str = None) -> str:
    """Using the file command to retrieve the mime type of a given file.

    :param path:
    :return:
    """
    return run_command("file -b --mime-type {}".format(path))

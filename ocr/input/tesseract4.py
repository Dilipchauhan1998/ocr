# -*- coding: utf-8 -*-
def to_text(path, language="eng+mar"):
    """Wraps Tesseract 4 OCR with custom language model.

    Parameters
    ----------
    path : str
        path of electronic invoice in JPG or PNG format

    Returns
    -------
    extracted_str : str
        returns extracted text from image in JPG or PNG format

    """
    import subprocess
    from distutils import spawn
    import tempfile
    import time

    # Check for dependencies. Needs Tesseract and Imagemagick installed.
    if not spawn.find_executable("tesseract"):
        raise EnvironmentError("tesseract not installed.")
    if not spawn.find_executable("convert"):
        raise EnvironmentError("imagemagick not installed.")
    if not spawn.find_executable("gs"):
        raise EnvironmentError("ghostscript not installed.")

    with tempfile.NamedTemporaryFile(suffix=".tiff") as tf:
        magick_cmd = [
            "convert",
            path,
            "-colorspace",
            "gray",
            "-type",
            "grayscale",
            "-contrast-stretch",
            "0",
            "-sharpen",
            "0x1",
            "tiff:-",
        ]

        p1 = subprocess.Popen(magick_cmd, stdout=subprocess.PIPE)

        tess_cmd = [
            "tesseract",
            "-l",
            language,
            "--oem",
            "1",
            "--psm",
            "3",
            "stdin",
            "stdout",
        ]
        p2 = subprocess.Popen(tess_cmd, stdin=p1.stdout, stdout=subprocess.PIPE)

        out, err = p2.communicate()

        extracted_str = out

        return extracted_str

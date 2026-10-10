import os
from pathlib import Path

import PIL.Image
import pytest

from mflux.utils.image_util import ImageUtil


@pytest.mark.fast
def test_save_image_propagates_write_failure(tmp_path):
    """A failure to write the image itself must propagate (issue #830).

    Previously the exception was logged and swallowed, so CLIs exited 0
    with no output file. Callers and the process must now see the error.
    """
    image = PIL.Image.new("RGB", (8, 8), color="red")
    readonly = tmp_path / "readonly"
    readonly.mkdir()
    os.chmod(readonly, 0o555)
    target = readonly / "out.png"

    with pytest.raises(OSError):
        ImageUtil.save_image(image, target)

    assert not target.exists()


@pytest.mark.fast
def test_save_image_succeeds_when_path_is_writable(tmp_path):
    image = PIL.Image.new("RGB", (8, 8), color="blue")
    target = tmp_path / "out.png"

    ImageUtil.save_image(image, target)

    assert target.exists()
    assert PIL.Image.open(target).size == (8, 8)

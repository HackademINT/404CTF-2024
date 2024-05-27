import numpy as np
from fl.types import Matrix, Vector


def apply_patch(
        image: Vector[np.float_],
        patch: Matrix[np.float_],
        edge: (int, int),
        image_length: int = 28
) -> Vector[np.float_]:
    image_patched = np.copy(image)
    for i in range(len(patch)):
        for j in range(len(patch[0])):
            image_patched[(edge[0] + i) * image_length + edge[1] + j] = patch[i][j]
    return image_patched

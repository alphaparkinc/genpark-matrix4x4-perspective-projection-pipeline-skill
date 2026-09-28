"""4x4 Transformation Matrix & Perspective Projection Pipeline
100% Python Standard Library (math).
"""

import math

class TransformPipeline4x4:
    """Homogeneous 4x4 graphics matrix transformer."""
    @staticmethod
    def perspective(fov_rad, aspect, near, far):
        f = 1.0 / math.tan(fov_rad / 2.0)
        return [
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ]

    @staticmethod
    def project_point(mat, pt):
        x, y, z = pt
        clip_x = mat[0][0]*x + mat[0][1]*y + mat[0][2]*z + mat[0][3]
        clip_y = mat[1][0]*x + mat[1][1]*y + mat[1][2]*z + mat[1][3]
        clip_z = mat[2][0]*x + mat[2][1]*y + mat[2][2]*z + mat[2][3]
        clip_w = mat[3][0]*x + mat[3][1]*y + mat[3][2]*z + mat[3][3]

        if clip_w != 0:
            return [round(clip_x / clip_w, 4), round(clip_y / clip_w, 4), round(clip_z / clip_w, 4)]
        return [clip_x, clip_y, clip_z]

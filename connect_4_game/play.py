from scipy.signal import convolve2d
import numpy as np

horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


def check_for_valid_game_board(game_board, player):
    for kernel in detection_kernels:
        if (convolve2d(game_board == player, kernel, mode="valid") == 4).any():
            return True
    return False

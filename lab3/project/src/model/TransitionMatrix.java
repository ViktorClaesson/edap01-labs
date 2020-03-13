package model;

public class TransitionMatrix {
    private int rows;
    private int cols;
    private int heads;
    private double[][] matrix;

    public TransitionMatrix(int rows, int cols, int heads) {
        this.rows = rows;
        this.cols = cols;
        this.heads = heads;
        this.matrix = new double[rows * cols * heads][rows * cols * heads];
        buildMatrix();
    }

    // Build the matrix
    public void buildMatrix() {
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                for (int h = 0; h < heads; h++) {
                    /*
                     * Walls => r = 1..rows-2, c = 0 and h = 3 r = 0, c = 1..cols-2 and h = 0 r =
                     * 1..rows-2, c = cols-1 and h = 1 r = rows-1, c = cols = 1..cols-2 and h = 2
                     * 
                     * Corners => r = 0, c = 0 and h = 0 OR 3 r = rows-1, c = 0 and h = 2 OR 3 r =
                     * 0, c = cols-1 and h = 0 OR 1 r = rows-1, c = cols-1 and h = 1 OR 2
                     */

                    // Check all corners
                    if (r == 0 && c == 0) {
                        if (h == 0 || h == 3) {
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = 0.5;
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = 0.5;
                        } else {
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = (h == 1)
                                    ? 0.7
                                    : 0.3;
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = (h == 2)
                                    ? 0.7
                                    : 0.3;
                        }
                    } else if (r == rows - 1 && c == 0) {
                        if (h == 2 || h == 3) {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = 0.5;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = 0.5;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = (h == 0)
                                    ? 0.7
                                    : 0.3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = (h == 1)
                                    ? 0.7
                                    : 0.3;
                        }
                    } else if (r == 0 && c == cols - 1) {
                        if (h == 0 || h == 1) {
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = 0.5;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = 0.5;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = (h == 2)
                                    ? 0.7
                                    : 0.3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = (h == 3)
                                    ? 0.7
                                    : 0.3;
                        }
                    } else if (r == rows - 1 && c == cols - 1) {
                        if (h == 1 || h == 2) {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = 0.5;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = 0.5;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = (h == 0)
                                    ? 0.7
                                    : 0.3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = (h == 3)
                                    ? 0.7
                                    : 0.3;
                        }
                        // Check all walls
                    } else if (r == 0) {
                        if (h == 0) {
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = 1.0 / 3;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = (h == 2)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = (h == 1)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = (h == 3)
                                    ? 0.7
                                    : 0.15;
                        }
                    } else if (r == rows - 1) {
                        if (h == 2) {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = 1.0 / 3;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = (h == 0)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = (h == 1)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = (h == 3)
                                    ? 0.7
                                    : 0.15;
                        }
                    } else if (c == 0) {
                        if (h == 3) {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = 1.0 / 3;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = (h == 0)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = (h == 1)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = (h == 2)
                                    ? 0.7
                                    : 0.15;
                        }
                    } else if (c == cols - 1) {
                        if (h == 1) {
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = 1.0 / 3;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = 1.0 / 3;
                        } else {
                            matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = (h == 2)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = (h == 0)
                                    ? 0.7
                                    : 0.15;
                            matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = (h == 3)
                                    ? 0.7
                                    : 0.15;
                        }

                        // Fill the rest
                    } else {
                        matrix[r * cols * heads + c * heads + h][(r + 1) * cols * heads + c * heads + 2] = (h == 2)
                                ? 0.7
                                : 0.1;
                        matrix[r * cols * heads + c * heads + h][(r - 1) * cols * heads + c * heads] = (h == 0) ? 0.7
                                : 0.1;
                        matrix[r * cols * heads + c * heads + h][r * cols * heads + (c + 1) * heads + 1] = (h == 1)
                                ? 0.7
                                : 0.1;
                        matrix[r * cols * heads + c * heads + h][r * cols * heads + (c - 1) * heads + 3] = (h == 3)
                                ? 0.7
                                : 0.1;
                    }
                }
            }
        }
    }

    // Given a new location (nR, nC, nH), return the probability
    public double getProbability(int r, int c, int h, int nR, int nC, int nH) {
        return matrix[r * cols * heads + c * heads + h][nR * cols * heads + nC * heads + nH];
    }

    public double[][] transpose() {
        int size = rows * cols * heads;
        double[][] tmpMatrix = new double[size][size];
        for (int r = 0; r < size; r++) {
            for (int c = 0; c < size; c++) {
                tmpMatrix[r][c] = matrix[c][r];
            }
        }
        return tmpMatrix;
    }
}
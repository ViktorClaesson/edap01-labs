package model;

import java.util.ArrayList;

public class ObservationMatrices {
    private int rows;
    private int cols;
    private double[][] matrices;

    public ObservationMatrices(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
        this.matrices = new double[rows * cols + 1][rows * cols * 4];
        buildMatrices();
    }

    private void buildMatrices() {
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int obs = (r * cols) + c;
                ArrayList<Integer> firstRing = oneStepAway(r, c, obs);
                ArrayList<Integer> secondRing = twoStepAway(r, c, obs);
                for (int h = 0; h < 4; h++) {
                    matrices[obs][r * cols * 4 + c * 4 + h] = 0.1;
                    matrices[rows * cols][r * cols * 4 + c * 4 + h] = 1 - 0.1 - firstRing.size() * 0.05
                            - secondRing.size() * 0.025;
                }
            }
        }
    }

    // Returns a list of indices from the first surrounding ring
    private ArrayList<Integer> oneStepAway(int r, int c, int obs) {
        ArrayList<Integer> tmpList = new ArrayList<>();
        for (int row = r - 1; row < r + 2; row++) {
            for (int col = c - 1; col < c + 2; col++) {
                if (row >= 0 && col >= 0 && row < rows && col < cols) {
                    int idx = (row * cols) + col;
                    if (idx != obs) {
                        tmpList.add(idx);
                        for (int h = 0; h < 4; h++) {
                            matrices[obs][row * cols * 4 + col * 4 + h] = 0.05;
                        }
                    }
                }
            }
        }
        return tmpList;
    }

    // Returns a list of indices from the second surrounding ring
    private ArrayList<Integer> twoStepAway(int r, int c, int obs) {
        ArrayList<Integer> tmpList = new ArrayList<>();
        for (int row = r - 2; row < r + 3; row += 4) {
            for (int col = c - 2; col < c + 3; col++) {
                if (row >= 0 && col >= 0 && row < rows && col < cols) {
                    int idx = (row * cols) + col;
                    tmpList.add(idx);
                    for (int h = 0; h < 4; h++) {
                        matrices[obs][row * cols * 4 + col * 4 + h] = 0.025;
                    }
                }
            }
        }
        for (int col = c - 2; col < c + 3; col += 4) {
            for (int row = r - 1; row < r + 2; row++) {
                if (row >= 0 && col >= 0 && row < rows && col < cols) {
                    int idx = (row * cols) + col;
                    tmpList.add(idx);
                    for (int h = 0; h < 4; h++) {
                        matrices[obs][row * cols * 4 + col * 4 + h] = 0.025;
                    }
                }
            }
        }
        return tmpList;
    }

    public double getProbability(int r, int c, int x, int y) {
        if (r < 0 || c < 0) {
            return matrices[rows * cols][x * cols * 4 + y * 4];
        }
        return matrices[(r * cols) + c][x * cols * 4 + y * 4];
    }

    public double[] getObservation(int r, int c) {
        if (r < 0 || c < 0) {
            return matrices[rows * cols];
        }
        return matrices[(r * cols) + c];
    }
}
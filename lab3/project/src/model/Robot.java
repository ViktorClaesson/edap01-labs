package model;

import java.util.Random;

public class Robot {
    private int rows;
    private int cols;
    private TransitionMatrix T;
    private int[] position = { 1, 0, 3 };

    public Robot(int rows, int cols, TransitionMatrix T) {
        this.rows = rows;
        this.cols = cols;
        this.T = T;
    }

    public void makeMove() {
        int r = position[0];
        int c = position[1];
        int h = position[2];
        int[][] possibleMoves = { { r - 1, c, 0 }, { r + 1, c, 2 }, { r, c - 1, 3 }, { r, c + 1, 1 } };
        double[] probabilities = new double[4];
        for (int i = 0; i < possibleMoves.length; i++) {
            if (possibleMoves[i][0] >= 0 && possibleMoves[i][1] >= 0 && possibleMoves[i][0] < rows
                    && possibleMoves[i][1] < cols) {
                probabilities[i] = T.getProbability(r, c, h, possibleMoves[i][0], possibleMoves[i][1],
                        possibleMoves[i][2]);
            } else {
                probabilities[i] = -1.0;
            }
        }

        Random rand = new Random();
        double prob = rand.nextDouble();
        double sum = 0.0;
        for (int i = 0; i < probabilities.length; i++) {
            if (probabilities[i] > 0.0) {
                if (sum + probabilities[i] >= prob) {
                    for (int j = 0; j < 3; j++) {
                        position[j] = possibleMoves[i][j];
                    }
                    return;
                } else {
                    sum += probabilities[i];
                }
            }
        }
    }

    public int[] getPosition() {
        return position;
    }
}
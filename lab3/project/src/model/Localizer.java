package model;

import java.util.HashMap;
import java.util.Random;

import control.EstimatorInterface;

public class Localizer implements EstimatorInterface {
	private int rows;
	private int cols;
	private int heads;
	private TransitionMatrix T;
	private ObservationMatrices O;
	private Robot robot;
	private double[][] transT;
	private double[] f;
	private int t;
	private Random rand;
	private double distance;
	private double hits;
	private double[][] matrix;
	private double[] O_tPlusOne;
	private HashMap<Integer, Tuple> transformer = new HashMap<Integer, Tuple>();

	public Localizer(int rows, int cols, int heads) {
		this.rows = rows;
		this.cols = cols;
		this.heads = heads;
		this.T = new TransitionMatrix(rows, cols, heads);
		this.O = new ObservationMatrices(rows, cols);
		this.robot = new Robot(rows, cols, T);
		this.transT = this.T.transpose();
		this.f = new double[rows * cols * heads];
		for (int i = 0; i < this.f.length; i++) {
			this.f[i] = 1.0 / (rows * cols * heads);
		}
		this.t = 0;
		this.rand = new Random();
		this.distance = 0.0;
		this.hits = 0.0;
		this.matrix = new double[rows][cols];
		for (int r = 0; r < rows; r++) {
			for (int c = 0; c < cols; c++) {
				transformer.put(r * cols * heads + c * heads, new Tuple(r, c));
			}
		}
	}

	/*
	 * return the number of assumed rows, columns and possible headings for the grid
	 * a number of four headings makes obviously most sense... the viewer can handle
	 * four headings at maximum in a useful way.
	 */
	public int getNumRows() {
		return rows;
	}

	public int getNumCols() {
		return cols;
	}

	public int getNumHead() {
		return heads;
	}

	/*
	 * should trigger one step of the estimation, i.e., true position, sensor
	 * reading and the probability distribution for the position estimate should be
	 * updated one step after the method has been called once.
	 */
	public void update() {
		System.out.println("----- NEW UPDATE ------");
		System.out.println("Current time: " + t);
		// 1. move robot to new pose
		robot.makeMove();
		// 2. obtain sensor reading based on its actual position given the sensor
		// reading
		int[] sensorPos = getCurrentReading();

		if (sensorPos == null) {
			O_tPlusOne = O.getObservation(-1, -1);
		} else {
			O_tPlusOne = O.getObservation(sensorPos[0], sensorPos[1]);
		}
		// 3. Update forward-filtering (pos. estimate)
		forwardFiltering(O_tPlusOne);
		// 4. Update t
		t++;
		int[] robotPos = getCurrentTrueState();
		int[] bestGuess = getHighestGuess();
		if (bestGuess[0] == robotPos[0] && bestGuess[1] == robotPos[1]) {
			hits++;
		}
		distance += Math.abs(robotPos[0] - bestGuess[0]) + Math.abs(robotPos[1] - bestGuess[1]);
		System.out.println("Manhattan distance: " + distance / t);
		System.out.println("Hitrate: " + hits / t);

		// Used to achieve result in the report.
		// if(t == 400){
		// System.exit(0);
		// }
	}

	/*
	 * returns the currently known true position i.e., after one simulation step of
	 * the robot as (x,y)-pair.
	 */
	public int[] getCurrentTrueState() {
		return robot.getPosition();
	}

	/*
	 * returns the currently available sensor reading obtained for the true position
	 * after the simulation step returns null if the reading was "nothing" (whatever
	 * that stands for in your model)
	 */
	public int[] getCurrentReading() {
		int[] truePosition = getCurrentTrueState();
		double prob = rand.nextDouble();
		double probSum = getOrXY(-1, -1, truePosition[0], truePosition[1], 0);
		if (probSum >= prob) {
			return null;
		}
		double[] obs = O.getObservation(truePosition[0], truePosition[1]);
		for (int i = 0; i < obs.length; i += 4) {
			probSum += obs[i];
			if (probSum >= prob) {
				Tuple t = transformer.get(i);
				int[] tmp = { t.first(), t.second() };
				return tmp;
			}
		}
		return null;
	}

	/*
	 * returns the currently estimated (summed) probability for the robot to be in
	 * position (x,y) in the grid. The different headings are not considered, as it
	 * makes the view somewhat unclear.
	 */
	public double getCurrentProb(int x, int y) {
		int idx = x * cols * 4 + y * 4;
		double prob = 0.0;
		for (int i = 0; i < 4; i++) {
			prob += f[idx + i];
		}
		return prob;
	}

	/*
	 * returns the probability entry of the sensor matrices O to get reading r
	 * corresponding to position (rX, rY) when actually in position (x, y) (note
	 * that you have to take care of potentially necessary transformations from
	 * states i = <x, y, h> to positions (x, y)).
	 */
	public double getOrXY(int rX, int rY, int x, int y, int h) {
		return O.getProbability(rX, rY, x, y);
	}

	/*
	 * returns the probability entry (Tij) of the transition matrix T to go from
	 * pose i = (x, y, h) to pose j = (nX, nY, nH)
	 */
	public double getTProb(int x, int y, int h, int nX, int nY, int nH) {
		return T.getProbability(x, y, h, nX, nY, nH);
	}

	private void forwardFiltering(double[] O_t) {
		double[][] tmpMatrix = new double[transT.length][transT.length];
		double[] fTemp = new double[f.length];
		double alpha;
		double fSum = 0.0;

		for (int r = 0; r < O_t.length; r++) {
			for (int c = 0; c < transT[r].length; c++) {
				tmpMatrix[r][c] = O_t[r] * transT[r][c];
			}
		}

		for (int r = 0; r < tmpMatrix.length; r++) {
			double rowSum = 0.0;
			for (int c = 0; c < tmpMatrix[r].length; c++) {
				rowSum += f[c] * tmpMatrix[r][c];
			}
			fTemp[r] = rowSum;
			fSum += rowSum;
		}

		f = fTemp;

		alpha = 1.0 / fSum;

		for (int i = 0; i < f.length; i++) {
			f[i] *= alpha;
		}
	}

	private int[] getHighestGuess() {
		for (int r = 0; r < rows; r++) {
			for (int c = 0; c < cols; c++) {
				matrix[r][c] = getCurrentProb(r, c);
			}
		}

		double max = -1;
		int[] highest = new int[2];
		for (int r = 0; r < rows; r++) {
			for (int c = 0; c < cols; c++) {
				if (matrix[r][c] > max) {
					max = matrix[r][c];
					highest[0] = r;
					highest[1] = c;
				}
			}
		}
		return highest;
	}
}
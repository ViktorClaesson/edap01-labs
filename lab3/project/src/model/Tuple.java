package model;

public class Tuple {
    private int first;
    private int second;

    public Tuple(int first, int second) {
        this.first = first;
        this.second = second;
    }

    public int first() {
        return first;
    }

    public int second() {
        return second;
    }
}
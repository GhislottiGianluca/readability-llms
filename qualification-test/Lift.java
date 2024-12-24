package tutorial;

public class Lift {

    private int topFloor;
    private int currentFloor = 0; // default
    private int capacity = 10;    // default
    private int numRiders = 0;    // default

    public Lift(int highestFloor) {
        if(highestFloor < 0) {
            throw new IllegalArgumentException("highestFloor should be non-negative");
        }
        topFloor = highestFloor;
    }

    public Lift(int highestFloor, int maxRiders) {
        this(highestFloor);
        if(maxRiders < 0) {
            throw new IllegalArgumentException("maxRiders should be non-negative");
        }
        capacity = maxRiders + numRiders;
    }

    public int getTopFloor() {
        return topFloor;
    }

    public int getCurrentFloor() {
        return currentFloor;
    }

    public int getCapacity() {
        return capacity;
    }

    public int getNumRiders() {
        return numRiders;
    }

    public boolean isFull() {
        return numRiders == capacity;
    }

    public void addRiders(int numEntering) {
        if(numEntering < 0) {
            throw new IllegalArgumentException("maxRiders should be positive");
        }
        if (numRiders + numEntering < capacity) {
            numRiders = numRiders + numEntering;
        } else {
            numRiders = capacity;
        }
    }

    private void goUp() {
        if (currentFloor < topFloor)
            currentFloor++;
    }

    private void goDown() {
        if (currentFloor > 0)
            currentFloor--;
    }

    public void call(int floor) {
        if (floor >= 0 && floor < topFloor) {
            while (floor != currentFloor) {
                if (floor > currentFloor)
                    goUp();
                else
                    goDown();
            }
        }
    }
}
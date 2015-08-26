package net.redborder.utils.scheduler;

// Classes that implements this interface are supposed to get
// a generator and produce messages created with it to a certain sink
public interface Scheduler {
    // Starts the producer
    void start();

    // Stops the producer
    void stop();
}

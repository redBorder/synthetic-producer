package net.redborder.utils.producers;

public interface IProducer {
    void send(String message, String key, int interval);
    String getPartitionKey();
}

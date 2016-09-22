package net.redborder.utils.producers;

public interface IProducer {
    void send(String message, String key);
    String getPartitionKey();
}
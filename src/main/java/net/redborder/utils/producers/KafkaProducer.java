package net.redborder.utils.producers;

import com.google.common.base.Joiner;
import com.google.gson.Gson;
import kafka.javaapi.producer.Producer;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;
import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

public class KafkaProducer implements IProducer {
    private static final Logger log = LoggerFactory.getLogger(KafkaProducer.class);

    private String brokersString, topic;
    private Producer<String, String> producer;

    // Connects to ZK, reads the broker data there, and builds
    // a string like the following: host1:9092,host2:9092.
    // After that, creates a kafka producer with that data.
    public KafkaProducer(String zkConnect, String topic) {
        // Set the topic
        this.topic = topic;

        // Connect to ZooKeeper
        RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3);
        CuratorFramework client = CuratorFrameworkFactory.newClient(zkConnect, retryPolicy);
        client.start();

        // Get the current kafka brokers and its IDs from ZK
        List<String> ids = Collections.emptyList();
        List<String> hosts = new ArrayList<>();

        try {
            ids = client.getChildren().forPath("/brokers/ids");
        } catch (Exception ex) {
            log.error("Couldn't get brokers ids", ex);
        }

        // Get the host and port from each of the brokers
        for (String id : ids) {
            String jsonString = null;

            try {
                jsonString = new String(client.getData().forPath("/brokers/ids/" + id), "UTF-8");
            } catch (Exception ex) {
                log.error("Couldn't parse brokers data", ex);
            }

            if (jsonString != null) {
                try {
                    Gson gson = new Gson();
                    Map json = gson.fromJson(jsonString, Map.class);
                    Double port = (Double) json.get("port");
                    String host = json.get("host") + ":" + port.intValue();
                    hosts.add(host);
                } catch (NullPointerException e) {
                    log.error("Failed converting a JSON tuple to a Map class", e);
                }
            }
        }

        // Close the zookeeper connection
        client.close();

        // Builds the brokers string
        brokersString = Joiner.on(',').join(hosts);

        // Set the kafka properties for the producer
        Properties props = new Properties();
        props.put("metadata.broker.list", brokersString);
        props.put("serializer.class", "kafka.serializer.StringEncoder");
        props.put("request.required.acks", "1");
        props.put("message.send.max.retries", "60");
        props.put("retry.backoff.ms", "1000");
        props.put("producer.type", "async");
        props.put("queue.buffering.max.messages", "10000");
        props.put("queue.buffering.max.ms", "500");
        props.put("partitioner.class", "net.redborder.utils.producers.SimplePartitioner");

        // Create the producer
        ProducerConfig config = new ProducerConfig(props);
        producer = new Producer<>(config);
    }

    @Override
    public void send(String message) {
        KeyedMessage<String, String> keyedMessage = new KeyedMessage<>(topic, message);
        producer.send(keyedMessage);
    }
}

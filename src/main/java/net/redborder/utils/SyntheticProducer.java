package net.redborder.utils;

import net.redborder.utils.generators.MessageGenerator;
import net.redborder.utils.producers.KafkaProducer;
import net.redborder.utils.scheduler.Scheduler;
import net.redborder.utils.scheduler.StandardScheduler;

import java.util.Map;

public class SyntheticProducer {
    public static void main(String[] args) {
        // Get the config file and parse it
        ConfigFile configFile = new ConfigFile(args[0]);

        // Create the generator
        Map<String, Object> fields = configFile.get("fields");
        MessageGenerator messageGenerator = new MessageGenerator(fields);

        // Create the producers
        String zkConnect = configFile.get("zk_connect");
        String topic = configFile.get("topic");
        KafkaProducer kafkaProducer = new KafkaProducer(zkConnect, topic);

        // Create the scheduler
        int rate = configFile.get("rate");
        int threads = configFile.get("threads");
        Scheduler scheduler = new StandardScheduler(messageGenerator, kafkaProducer, rate, threads);
        scheduler.start();

        // Shutdown hooks
        // ...
    }
}
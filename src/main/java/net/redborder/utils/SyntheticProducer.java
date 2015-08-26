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
        KafkaProducer kafkaProducer = new KafkaProducer(zkConnect);

        // Create the scheduler
        Scheduler scheduler = new StandardScheduler(messageGenerator, kafkaProducer);
        scheduler.start();

        // Shutdown hooks
        // ...
    }
}
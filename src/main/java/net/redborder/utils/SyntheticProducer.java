package net.redborder.utils;

import net.redborder.utils.generators.MessageGenerator;
import net.redborder.utils.producers.KafkaProducer;
import net.redborder.utils.scheduler.Scheduler;
import net.redborder.utils.scheduler.StandardScheduler;
import org.apache.commons.cli.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

public class SyntheticProducer {
    public static Logger log = LoggerFactory.getLogger(SyntheticProducer.class);

    public static void main(String[] args) {
        Options options = new Options();
        options.addOption("r", "rate", true, "messages rate per second");
        options.addOption("t", "threads", true, "number of producer threads");
        options.addOption("c", "config", true, "config file path");
        options.addOption("z", "zookeeper", true, "zookeeper connect string");
        options.addOption("h", "help", false, "show this help");

        CommandLineParser parser = new BasicParser();
        HelpFormatter helpFormatter = new HelpFormatter();
        CommandLine cmdLine = null;

        try {
            cmdLine = parser.parse(options, args);
        } catch (ParseException e) {
            log.error("One or more of the options specified are not allowed. Check the options and try again.");
            System.exit(1);
        }

        if (cmdLine.hasOption("h") || !cmdLine.hasOption("r") || !cmdLine.hasOption("t") ||
                !cmdLine.hasOption("c") || !cmdLine.hasOption("z")) {
            helpFormatter.printHelp("java -jar synthetic-producer.jar", options);
            System.exit(1);
        }

        // Get the config file and parse it
        ConfigFile configFile = new ConfigFile(cmdLine.getOptionValue("config"));

        // Create the generator
        Map<String, Object> fields = configFile.get("fields");
        MessageGenerator messageGenerator = new MessageGenerator(fields);

        // Create the producers
        String zkConnect = cmdLine.getOptionValue("zookeeper");
        String topic = configFile.get("topic");
        KafkaProducer kafkaProducer = new KafkaProducer(zkConnect, topic);

        // Create the scheduler
        int rate = Integer.valueOf(cmdLine.getOptionValue("rate"));
        int threads = Integer.valueOf(cmdLine.getOptionValue("threads"));
        Scheduler scheduler = new StandardScheduler(messageGenerator, kafkaProducer, rate, threads);
        scheduler.start();

        // Shutdown hooks
        // ...
    }
}
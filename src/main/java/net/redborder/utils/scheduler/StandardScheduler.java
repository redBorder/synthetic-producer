package net.redborder.utils.scheduler;

import net.redborder.utils.generators.Generator;
import net.redborder.utils.producers.IProducer;
import org.codehaus.jackson.map.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;

public class StandardScheduler implements Scheduler {
    private final static Logger log = LoggerFactory.getLogger(StandardScheduler.class);

    private final Generator generator;
    private final IProducer producer;
    private final SenderThread senderThread = new SenderThread();

    public StandardScheduler(Generator generator, IProducer producer) {
        this.generator = generator;
        this.producer = producer;
    }

    @Override
    public void start() {
        senderThread.start();
    }

    @Override
    public void stop() {
        senderThread.interrupt();
    }

    private class SenderThread extends Thread {
        @Override
        public void run() {
            while (!currentThread().isInterrupted()) {
                Map<String, Object> message = generator.generate();
                ObjectMapper objectMapper = new ObjectMapper();

                try {
                    String json = objectMapper.writeValueAsString(message);
                    producer.send(json);
                    currentThread().sleep(1000);
                } catch (InterruptedException e) {
                    // Interrupted while waiting, just exit...
                } catch (IOException e) {
                    log.error("Couldn't serialize message message {}", message);
                    currentThread().interrupt();
                }
            }
        }
    }
}

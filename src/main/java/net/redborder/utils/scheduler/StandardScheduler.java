package net.redborder.utils.scheduler;

import com.codahale.metrics.ConsoleReporter;
import com.codahale.metrics.Meter;
import com.codahale.metrics.MetricRegistry;
import com.google.common.util.concurrent.RateLimiter;
import com.google.gson.Gson;
import net.redborder.utils.generators.Generator;
import net.redborder.utils.producers.IProducer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class StandardScheduler implements Scheduler {
    private final static Logger log = LoggerFactory.getLogger(StandardScheduler.class);
    private final static MetricRegistry metrics = new MetricRegistry();

    private final Generator generator;
    private final IProducer producer;
    private final RateLimiter rateLimiter;
    private final List<SenderThread> senderThreads;
    private final Meter messages = metrics.meter("messages");

    public StandardScheduler(Generator generator, IProducer producer, int rate, int threads) {
        this.generator = generator;
        this.producer = producer;
        this.rateLimiter = RateLimiter.create(rate);

        // Create the threads that will send the events
        this.senderThreads = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            senderThreads.add(new SenderThread());
        }

        // Report the metrics of messages produced
        ConsoleReporter reporter = ConsoleReporter.forRegistry(metrics)
                .convertRatesTo(TimeUnit.SECONDS)
                .convertDurationsTo(TimeUnit.MILLISECONDS)
                .build();

        reporter.start(5, TimeUnit.SECONDS);
    }

    @Override
    public void start() {
        for (SenderThread senderThread : senderThreads) {
            senderThread.start();
        }
    }

    @Override
    public void stop() {
        for (SenderThread senderThread : senderThreads) {
            senderThread.interrupt();
        }
    }

    private class SenderThread extends Thread {
        @Override
        public void run() {
            Gson gson = new Gson();

            while (!currentThread().isInterrupted()) {
                Map<String, Object> message = generator.generate();
                String json = gson.toJson(message);
                rateLimiter.acquire();
                producer.send(json);
                messages.mark();
            }
        }
    }
}

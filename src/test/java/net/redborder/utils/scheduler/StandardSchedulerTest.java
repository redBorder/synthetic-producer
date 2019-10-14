package net.redborder.utils.scheduler;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import static org.mockito.MockitoAnnotations.initMocks;

import java.util.HashMap;
import java.util.Map;
import net.redborder.utils.producers.IProducer;
import org.junit.Before;
import org.junit.Test;

public class StandardSchedulerTest {

    private Map<String, Object> message;

    private IProducer producer;

    private StandardScheduler standardScheduler;

    @Before
    @SuppressWarnings("unchecked")
    public void before() throws Exception {

        message = new HashMap<>();
        message.put("id", "123");
        message.put("nested", new HashMap<String, Object>());
        ((Map<String, Object>) message.get("nested")).put("id", "345");

        producer = mock(IProducer.class);

        standardScheduler = new StandardScheduler(null, producer, 1D, 1);
    }

    @Test
    public void extractPartitionKey() {
        when(producer.getPartitionKey()).thenReturn("id");
        String result = standardScheduler.extractPartitionKey(message);
        assertEquals("123", result);

        when(producer.getPartitionKey()).thenReturn("nested.id");
        result = standardScheduler.extractPartitionKey(message);
        assertEquals("345", result);
    }
}

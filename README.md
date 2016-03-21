# synthetic-producer
[![Codacy Badge](https://api.codacy.com/project/badge/grade/75478e4c803148978811f05f732f3f3a)](https://www.codacy.com/app/redBorder/synthetic-producer)
Generates random JSON messages and sends them to Apache Kafka.
It uses Apache Zookeeper to discover the available brokers and partitions for a given topic.

Usage:

```bash
$ java -jar target/synthetic-producer-1.1-selfcontained.jar
usage: java -jar synthetic-producer.jar
 -c,--config <arg>      config file path
 -h,--help              show this help
 -r,--rate <arg>        messages rate per second
 -t,--threads <arg>     number of producer threads
 -z,--zookeeper <arg>   zookeeper connect string
```

## Config file

The config file specifies the Zookeeper connection string, the rate of 
messages generated, the threads to use, the topic where you want to produce,
and the messages' schema.

For example, take a look at the following config:

```yaml
topic: testTopic
fields:
  myConstant:
    type: constant
    value: 'Hello, World!'
  randomNumber:
    type: integer
    min: 0
    max: 100
```

Using a file like that will make the producer will connect to Zookeeper at "localhost:2181" in order create
two producing threads, and send messages to the topic "testTopic" at a constant rate of 100 msgs per
second, which would look like the following:

```
{ "myConstant": "Hello, World!", "randomNumber": 4}
{ "myConstant": "Hello, World!", "randomNumber": 12}
{ "myConstant": "Hello, World!", "randomNumber": 94}
{ "myConstant": "Hello, World!", "randomNumber": 33}
```

You can find a full example of config file in [this file](https://github.com/redBorder/synthetic-producer/blob/master/configProducer.yml)

## Fields types

You can use a variety of different field types to generate your random message.
Some types accepts one or more parameters that modify the field randomness.
For example, the constant type always generates the same value for a field, but the integer
type generates a random number between 'min' and 'max' for each field.

The available types, with their parameters, are the following:

### constant
Generates a constant value

Parameters:
 - value: The value to be generated
 
Example:
```yaml
myField:
 type: constant
 value: "This is a constant"
```
 
### integer
Generates a random integer

Parameters:
- min: The minimum integer to be generated (Default 0)
- max: The maximum integer to be generated (Default Integer.MAX_VALUE)
- negative: True if the generated number must be negative (It will be multiplied by -1)

Example:
```yaml
myField:
  type: integer
  min: 0
  max: 50
```

### ip
Generates a random IP address

Parameters:
- min: The minimum ip to be generated (Default 0.0.0.0)
- max: The maximum ip to be generated (Default 255.255.255.255)

Example:
```yaml
myField:
  type: ip
  min: 192.168.0.1
  max: 192.168.0.255
```

### mac
Generates a random MAC address

Parameters:
- min: The minimum ip to be generated (Default 00:00:00:00:00:00)
- max: The maximum ip to be generated (Default FF:FF:FF:FF:FF:FF)

Example:
```yaml
myField:
  type: mac
  min: 00:00:00:00:00:11
  max: 00:00:00:00:00:44
```

### timestamp
Generates a field with the current timestamp of the machine

Example:
```yaml
myField:
  type: timestamp
```

### collection
Generates a random element from the given collection of elements

Parameters:
- values: An array of elements

Example:
```yaml
myField:
  type: collection
  values:
    - Campus A
    - Campus B
    - Campus C
    - Campus D
    - Campus E
```

### composition
Generates a random field based on a composition of two or more random fields

Parameters:
- separator: The character that will be used as the separator between the two generated values
- components: An array of types definitions that will be generated before joining the result with the separator

Examples:
```yaml
myField:
  type: composition
  separator: ':'
  components:
    - type: integer
      min: 0
      max: 11
    - type: integer
      min: 0
      max: 101
```

This will create values like the following: 2:34, 6:11, 1:75, 10:62...
Of course, you can use a composition type as a component for another composition type.

## Contributing

1. [Fork it](https://github.com/redborder/synthetic-producer/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## License

[AGPL v3](http://www.gnu.org/licenses/agpl-3.0.html)

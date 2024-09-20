from kafka import KafkaProducer

KAFKA_BROKER = '52.78.171.52:9092'
PROTOCOL = 'PLAINTEXT'

class Producer:
    
    def __init__(self, topic: str) -> None:
        self.topic = topic
        
    def configuration(self):
        return KafkaProducer(
            bootstrap_servers = KAFKA_BROKER,  # 브로커 IP 주소
            security_protocol = PROTOCOL,  # 보안 프로토콜 설정
            value_serializer=lambda v: str(v).encode('utf-8')
        )
        
    def send(self, message: str): pass
    
class TestProducer(Producer):
    
    def __init__(self, topic: str) -> None:
        super().__init__(topic)
        
    def send(self, message: str):
        client = self.configuration()
        client.send(self.topic, message)
        client.flush()
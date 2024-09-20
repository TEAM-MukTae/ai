from kafka import KafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from database import summaries, keywords, records, workbooks
from myKafka.producer import TestProducer
from ai.openapi import MultiChoiceClient, SummaryClient
from datetime import datetime

WORKERS = 5
# KAFKA_BROKER = f'{os.environ.get('KAFKA-IP')}:9092'
KAFKA_BROKER = f'52.78.171.52:9092'
PROTOCOL = 'PLAINTEXT'
DESERIALIZER = lambda x : x.decode('UTF-8')

class Consumer:
    
    def __init__(self, topic: str) -> None:
        self.topic = topic
        self.running = False
        
    def configuration(self):
        return KafkaConsumer(
            self.topic,
            bootstrap_servers = KAFKA_BROKER,  # 브로커 IP 주소
            security_protocol = PROTOCOL,  # 보안 프로토콜 설정
            value_deserializer = lambda x: x.decode('utf-8')  # 값 역직렬화 설정
        )
        
    def close(self):
        self.running = False
        
    def run(self): 
        pass
    

class TestConsumer(Consumer):
    
    def __init__(self, topic: str) -> None:
        super().__init__(topic)
        
    def run(self):
        
        client = self.configuration()
        key = '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'
        # c1 = TestClient(SUMMARIZATION, "You're Summarization Machine!", key = key)
        c1 = SummaryClient()
        
        self.running = True
        with ThreadPoolExecutor(WORKERS) as executor:
            
            try:
                while self.running:
                    for message in client:
                        if not message or message == '': continue
                        data = message.value
                        
                        result = c1.request([data])
                        # print(data)
                        # print(result)
                        # print(result["summarization"])
                        # print(result["keywords"])
                        rs_id = summaries.insert_summaries(2, result["summarization"])
                        print(rs_id)
                        if rs_id > 0: keywords.insert_keywords(rs_id, result['keywords'])
                        
                        
            except KeyboardInterrupt:
                print(f'Error occured while consuming topic {self.topic}')
                
            finally:
                client.close()


class SummaryConsumer(Consumer):
        
    def __init__(self) -> None:
        topic = 'summary'
        super().__init__(topic)
        
    def run(self):
        
        client = self.configuration()
        c1 = SummaryClient()
        pd = TestProducer('summary_done')
        
        self.running = True
        with ThreadPoolExecutor(WORKERS) as executor:
            try:
                while self.running:
                    for message in client:
                        if not message or message == '': continue
                        r_id = message.value
                        print('Summary', r_id)

                        record = records.fetch_records_one(r_id)
                        if 'transcript' not in record: continue
                        print(record)
                        
                        data = record['transcript']
                        result = c1.request([data])
                        print(result)
                        
                        rs_id = summaries.insert_summaries(r_id, result["summarization"])
                        print(rs_id)
                        if rs_id > 0: keywords.insert_keywords(rs_id, result['keywords'])
                        pd.send(rs_id)
                        
            except KeyboardInterrupt:
                print(f'Error occured while consuming topic {self.topic}')
                
            finally:
                client.close()


class WorkbookConsumer(Consumer):
        
    def __init__(self) -> None:
        topic = 'problem'
        super().__init__(topic)
        
    def run(self):
        client = self.configuration()
        c1 = MultiChoiceClient()
        pd = TestProducer('problem_done')
        
        self.running = True
        with ThreadPoolExecutor(WORKERS) as executor:
            try:
                while self.running:
                    for message in client:
                        if not message or message == '': continue
                        raw_text = message.value
                        print('Workbook', raw_text)
                        
                        result = c1.request([raw_text, '5', 'English'])
                        
                        today = datetime.today().strftime('%Y-%m-%d')
                        w_id = workbooks.insert_workbooks(1, today, str(result))
                        pd.send(w_id)
                        print(w_id, result)
                        
            except KeyboardInterrupt:
                print(f'Error occured while consuming topic {self.topic}')
                
            finally:
                client.close()
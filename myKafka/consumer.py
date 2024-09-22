from kafka import KafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from database import summaries, keywords, records, workbooks
from myKafka.producer import TestProducer
from ai.openapi import MultiChoiceClient, SummaryClient
from datetime import datetime
from document.s3 import extract_text_from_pdf
import json

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
        c1 = SummaryClient()
        
        self.running = True            
        try:
            while self.running:
                for message in client:
                    if not message or message == '': continue
                    data = message.value
                    
                    result = c1.request([data])
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
        
        try:
            while self.running:
                for message in client:
                    if not message or message == '': continue
                    r_id = json.loads(message.value)
                    print('Summary', r_id)

                    record = records.fetch_records_one(r_id)
                    if 'transcript' not in record: continue
                    print(record)
                    
                    data = record['transcript']
                    result = c1.request([data])
                    print(result)
                    
                    summary = ""
                    for sentence in result["summarization"]:
                        summary += f"{sentence}<br/>"
                    
                    response = {
                        "id": r_id,
                        "summary": summary,
                        "keywords": result['keywords']
                    }
                    
                    pd.send(json.dumps(response, ensure_ascii = False ))
                    
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
        try:
            while self.running:
                for message in client:
                    if not message or message == '': continue
                    requestObject = json.loads(message.value)
                    print(requestObject)
                    idList = requestObject['idList']
                    urlList = requestObject['urlList']
                    print(idList, urlList)
                    
                    dataList = records.fetch_records(idList)
                    # for id in idList: dataList.append(records.fetch_records_one(id))
                    
                    if len(dataList) == 0: continue
                    userID = dataList[0]['u_id']
                    print(dataList)
                    
                    text_merged = '[0]'
                    for url in urlList:
                        text_merged += f'{extract_text_from_pdf(url)}\n'
                    if text_merged == "": continue
                    
                    text_merged += '\n[1]'
                    for data in dataList: text_merged += f'{data["transcript"]}\n'
                    print(text_merged)
                          
                    count = 5
                    # # count = requestObject['count']
                    # language = 'Ko'
                    
                    language = requestObject['language']
                    result = c1.request([text_merged, f'{count}', f'{language}'])
                    response = {
                        "userId": userID,
                        "title": "임시 타이틀 (연결되면 바꿈)",
                        "questions": result["questions"]   
                    }
                    
                    print(response)
                    pd.send(json.dumps(response, ensure_ascii = False ))
                    print('Response sent to Problem Done')
                    
        except KeyboardInterrupt:
            print(f'Error occured while consuming topic {self.topic}')
            
        finally:
            client.close()
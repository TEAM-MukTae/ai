from myKafka.consumer import TestConsumer
from myKafka.producer import TestProducer
from database.records import fetch_records
from database.workbooks import insert_workbooks

def test_produce():
    text = "2"
    c1 = TestProducer('summary')
    c1.send(text)
    
def test_problem():
    text = "JDK 7에서는 자바 언어에 상당한 변화가 계획되어 있었으나 JDK 7로 예정되었던 변화가 JDK 7과 JDK 8로 나뉘면서 JDK 7에는 상대적으로 사소한 언어 특성만이 추가되었다. 구체적으로 이진수 표기 추가, 가독성을 위해 수 표기에 밑줄(underscore)을 허용, 스위치 문(switch에서 문자열 사용, 제네릭 타입 객체 생성 시 타입 추론(type inference), 자동 자원 해제를 위한 try 문법, 여러 예외 타입을 동시에 잡도록 허용하는 문법 등이 추가되었다. JDK 9는 사업적으로 엄청난 변화가 있었다. 언어적인 변화보단 사용방법이 바뀌었다. 먼저 사업적으로 사용이 안된다. 이게 무슨뜻이냐면 Java 8 까진 사업적으로 가능한데 JDK 9부터 안된다는 뜻이다. 한마디로 돈을 받고 Java 프로그램을 팔수 없게된다. 하지만 사업이 아닌 개인용 & 학생용은 16까지 가능하다"
    c1 = TestProducer('problem')
    c1.send(text)
    
    
def test_fetch_records():
    print(fetch_records([2, 3, 4]))
    
def test_insert_workbooks():
    print(insert_workbooks(1, 'Test Title', 'Test Problem Set'))
    
test_problem()
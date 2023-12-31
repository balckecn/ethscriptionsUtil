import requests
import hashlib
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class RandomNumberGenerator:
    def __init__(self, start, end):
        self.numbers = list(range(start, end + 1))

    def get_random_number(self):
        if not self.numbers:
            return None  # 所有数字都已经被选择完毕
        index = random.randint(0, len(self.numbers) - 1)
        random_number = self.numbers.pop(index)
        return random_number


def get_channel_messages(data):

    # 将data转为hash
    hash = hashlib.sha256(data.encode('utf-8')).hexdigest()

    # 构建请求URL
    url = f"https://ethscriber.xyz/api/ethscriptions/exists/{hash}"


    # 发送 GET 请求, 获取是否存在
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        if result["result"]:
            # 若已经存在的不想打印的话，直接注释掉下面这行
            print(f"{data} 已经存在")
        else:
            print(f"{data} 不存在，可以打，赶紧的")
            hex_representation = hex(int.from_bytes(data.encode(), 'big'))
            print(f"HEX为： {hex_representation}")
            return None
    else:
        print(f"Failed to get messages. Status code: {response.status_code}")
        return None

def main(start, end):
    # 自行替换需要打的data
    # 注意，换成了需要打的data之后，需要将 id: 后面的值 改为 "{}"
    data_template = 'data:,{{"p":"erc-20","op":"mint","tick":"𝕏","id":"{}","amt":"1000"}}'

    # 构建数组，不用管
    rng = RandomNumberGenerator(start, end)

    # 创建一个 ThreadPoolExecutor，指定线程数为 5（可以根据需要调整）
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        for _ in range(start, end):
            num = rng.get_random_number()
            data = data_template.format(num)
            # 提交任务到线程池中，使用 submit 方法，每次循环返回一个 Future 对象
            future = executor.submit(get_channel_messages, data)
            futures.append(future)

        # 等待所有任务完成
        for future in as_completed(futures):
            result = future.result()
            # 在这里可以对结果进行处理，如果不需要处理结果，可以忽略这一部分

if __name__ == "__main__":
    start = 0;
    end = 20001;
    main(start, end)

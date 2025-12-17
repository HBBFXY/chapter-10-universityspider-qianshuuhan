import requests
from bs4 import BeautifulSoup
import csv

class UniversityRankSpider:
    def __init__(self, base_url):
        self.base_url = base_url  # 排名网站的基础URL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.all_universities = []  # 存储所有高校信息

    def fetch_page(self, page_num):
        """请求指定页码的页面"""
        url = f"{self.base_url}?page={page_num}"  # 假设页面参数为page
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 抛出HTTP错误
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"请求第{page_num}页失败：{e}")
            return None

    def parse_page(self, html):
        """解析页面，提取高校排名信息"""
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="rank-table")  # 假设表格类名为rank-table
        rows = table.find_all("tr")[1:]  # 跳过表头行

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                rank = cols[0].text.strip()
                name = cols[1].text.strip()
                score = cols[2].text.strip()
                self.all_universities.append({
                    "排名": rank,
                    "学校名称": name,
                    "得分": score
                })

    def crawl_all_pages(self, total_pages):
        """爬取所有页码的信息"""
        for page in range(1, total_pages + 1):
            print(f"正在爬取第{page}页...")
            html = self.fetch_page(page)
            if html:
                self.parse_page(html)
        print(f"爬取完成，共获取{len(self.all_universities)}所高校信息")

    def save_to_csv(self, filename):
        """将结果保存到CSV文件"""
        if not self.all_universities:
            print("无数据可保存")
            return
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.all_universities[0].keys())
            writer.writeheader()
            writer.writerows(self.all_universities)
        print(f"数据已保存到{filename}")


# 示例使用（需替换为实际排名网站的URL）
if __name__ == "__main__":
    # 注意：实际使用时需替换为合法的公开大学排名网站URL
    base_url = "https://example.com/university-rank"  # 示例URL，需替换
    spider = UniversityRankSpider(base_url)
    spider.crawl_all_pages(total_pages=20)  # 假设共20页
    spider.save_to_csv("university_rank.csv")

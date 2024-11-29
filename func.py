import requests
from bs4 import BeautifulSoup
from company_aliases import alias_mapping
#Hàm tìm mã cổ phiếu dựa vào tên của công ty
def get_stock_name(company_name):
    # Tìm mã cổ phiếu từ Yahoo Finance
    def get_ticker_Yafi(company_name):
        yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        params = {"q": company_name, "quotes_count": 1, "country": "all"}

        try:
            res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
            data = res.json()

            # Kiểm tra dữ liệu trả về
            if 'quotes' in data and len(data['quotes']) > 0:
                company_code = data['quotes'][0]['symbol']
                return company_code
            else:
                return None  # Trả về None nếu không tìm thấy mã cổ phiếu
        except Exception as e:
            print(f"Error retrieving data for {company_name}: {e}")
            return None  # Trả về None nếu có lỗi trong quá trình truy vấn
    
    # Tìm mã cổ phiếu từ StockMonitor (chỉ dùng khi Yahoo Finance không tìm thấy vì sẽ chậm hơn)
    def get_ticker_StMo(company_name):
        sectors = [
            "healthcare",
            "basic materials",
            "communication services",
            "consumer cyclical",
            "consumer defensive",
            "energy",
            "financial services",
            "industrials",
            "technology",
            "utilities"
        ]

        base_url = "https://www.stockmonitor.com/sector/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        def get_stock_symbol_by_name(sector_url, company_name):
            try:
                response = requests.get(sector_url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    rows = soup.find_all('tr')
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) > 2:
                            stock_symbol = cells[1].text.strip()
                            stock_name = cells[2].text.strip()
                            if company_name.lower() in stock_name.lower():
                                return stock_symbol
                else:
                    print(f"Lỗi khi truy cập URL: {sector_url} - {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Yêu cầu bị lỗi: {e}")
                return None

        # Duyệt qua các sector và tìm công ty
        for sector in sectors:
            sector_url = f"{base_url}{sector.replace(' ', '-').lower()}/" 
            symbol = get_stock_symbol_by_name(sector_url, company_name)
            if symbol:
                return symbol

        return None

    # Gọi hàm get_ticker_Yafi trước, nếu không có kết quả, gọi get_ticker_StMo
    full_company_name = alias_mapping.get(company_name.lower(), company_name)#Dùng alias để ánh xạ tên input và tên trong aliases
    symbol = get_ticker_Yafi(full_company_name)
    if symbol:
        return symbol
    else:
        return get_ticker_StMo(full_company_name)


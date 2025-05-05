import httpx
from app.config import settings

class AlpacaClient:
    def __init__(self):
        self.base_url = settings.ALPACA_BASE_URL
        self.data_url = settings.ALPACA_DATA_URL
        self.session = httpx.AsyncClient(
            headers={
                "accept": "application/json",
                "APCA-API-KEY-ID": settings.ALPACA_API_KEY,
                "APCA-API-SECRET-KEY": settings.ALPACA_SECRET_KEY,
            }
        )
    
    async def check_auth(self):
        response = await self.session.get(f"{self.base_url}/v2/account")       
        return response.json()

    async def submit_order(self, symbol, qty, side, order_type="limit", limit_price=None):
        payload = {
            "symbol": symbol,
            "qty":  str(qty),
            "side": side,
            "type": order_type,
            "time_in_force": "gtc",
            "limit_price": str(limit_price) if limit_price else None,           
        }        
        
        response = await self.session.post(f"{self.base_url}/v2/orders", json=payload)
        rlt = response.json()     
        if response.status_code == 200:
            print(f"Create : {rlt}")
            return {
                "success": True,
                "data": rlt,               
            }
        else:
            return {
                "success": False,
                "data": rlt,               
            }
              
    
    async def replace_order(self, order_id, qty, side, order_type="limit", limit_price=None):
        payload = {
            "qty":  str(qty),
            "side": side,
            "type": order_type,
            "time_in_force": "gtc",
            "limit_price": str(limit_price) if limit_price else None,           
        }
        response = await self.session.patch(f"{self.base_url}/v2/orders/{order_id}", json=payload)
        rlt = response.json()        
        if response.status_code == 200:
            print(f"Replace : {rlt}")
            return {
                "success": True,
                "data": rlt,               
            }
        else:
            print(f"Replace Error: {rlt}")
            return {
                "success": False,
                "data": rlt,               
            }
        
    
    async def get_orders(self):
        response = await self.session.get(f"{self.base_url}/v2/orders?status=all")
        rlt = response.json()
        response.raise_for_status()
        return rlt

    async def get_order_by_id(self, order_id):
        response = await self.session.get(f"{self.base_url}/v2/orders/{order_id}")
        rlt = response.json()
        response.raise_for_status()
        return rlt
    
    async def delete_order(self, order_id):
        response = await self.session.delete(f"{self.base_url}/v2/orders/{order_id}")
        
        if response.status_code == 200:
            return {
                "success": False,
        
            }
        else:
            return {
                "success": True,        
            }
                

    async def close_position(self, symbol):
        try:
            response = await self.session.delete(f"{self.base_url}/v2/positions/{symbol}")
            print(response)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None  # no open position
            elif e.response.status_code == 403:
                print(e.response.json())
                return None
    
                

    async def get_position(self, symbol):
        response = await self.session.get(f"{self.base_url}/v2/positions/{symbol}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    async def get_all_position(self):
        response = await self.session.get(f"{self.base_url}/v2/positions")
        rlt = response.json()
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return rlt

    async def get_last_quote(self, symbol):        
        response = await self.session.get(f"{self.data_url}/v2/stocks/{symbol}/quotes/latest")                        
        rlt = response.json()        
        if response.status_code == 404:
            print()
            return {
                "success": False,
                "data": rlt,               
            }
        else:
            return {
                "success": True,
                "data": rlt,               
            }
        
import asyncio
from datetime import datetime
from app.alpaca_client import AlpacaClient
from app.config import settings
from app.models import Webhook
from sqlalchemy.orm import Session

alpaca = AlpacaClient()

async def manage_order(symbol: str, action: str, quantity: int, price: int, db: Session):
    side = action.lower()    
    
    # position = await alpaca.get_position(symbol)
    # if position:
    #     pos_side = "buy" if float(position["qty"]) > 0 else "sell"
    #     if pos_side != side:
    #         await alpaca.close_position(symbol)

    order = {}
    status = ""
    order_id = ""
    webhook_record = Webhook(
        ticker      = symbol,
        action      = side,
        quantity    = quantity,
        price       = 0.0,
        date        = datetime.utcnow(),
        status      = "polling",        
    )
    db.add(webhook_record)
    for attempt in range(settings.RETRY_LIMIT + 1):
        quote = await alpaca.get_last_quote(symbol)
        if(quote["success"] == False):    
            print(f"Quote not found for symbol {symbol}")        
            webhook_record.message = f"Symbol {symbol} not found"
            db.commit()
            db.refresh(webhook_record)
            await asyncio.sleep(settings.RETRY_BACKOFF_SECONDS)
            continue        
        quote_data = quote.get("data", {})
        q = quote_data.get("quote", {})

        if attempt < 2:
            limit_price = (float(q["ap"]) + float(q["bp"])) / 2
        else:
            limit_price = float(q["bp"] if side == "buy" else q["ap"])

        limit_price = round(limit_price, 2)        

        print(f"Attempt {attempt + 1}: Limit Price: {limit_price}")

        # Done with Limit Price
        
        if order_id == "":
            print("Trying to Submit Order")
            orderResponse = await alpaca.submit_order(
                symbol      = symbol,
                qty         = quantity,
                side        = side,
                limit_price = limit_price,
                order_type  = "limit"
            )
            order = orderResponse.get("data", {})
            if orderResponse.get("success") == False:
                print(f"Order submission failed: {orderResponse.get('data', 'No reason')}")
                data = orderResponse.get("data", {})
                print(data.get("message", "No reason"))
                webhook_record.message = data.get("message", "No reason")
                await asyncio.sleep(settings.RETRY_BACKOFF_SECONDS)
                continue
            else:
                status = order.get("status", "").lower()
                order_id = order.get("id")
                webhook_record.order_id = order.get("id")
                webhook_record.status = status
                webhook_record.limit_price = limit_price
        

        else: 
            print("Trying to Replace Order: ", attempt + 1)
            
            current_order = await alpaca.get_order_by_id(order_id)
            current_status = current_order.get("status", "").lower()
            if(current_status == "filled" or current_status == "canceled"):
                print(f"Order already filled or canceled: {current_status}")
                webhook_record.status = current_status
                db.commit()
                db.refresh(webhook_record)
                return {
                    "id": str(webhook_record.id),
                    "status": str(webhook_record.status),
                }                

            print("Current Order: {}", current_order)

            #  Delete And Resubmit Order
            print("ORDER_ID", order_id)

            deleteResponse = await alpaca.delete_order(order_id)
            print(deleteResponse)
            if deleteResponse.get("success") == False:
                print(f"Order deletion failed: {deleteResponse.get('data', 'No reason')}")
                data = deleteResponse.get("data", {})
                print(data.get("message", "No reason"))
                webhook_record.message = data.get("message", "No reason")
                await asyncio.sleep(settings.RETRY_BACKOFF_SECONDS)
                continue
                
            print("Ready for ReSubmit", order_id)

            orderResponse = await alpaca.submit_order(
                symbol      = symbol,
                qty         = quantity,
                side        = side,
                limit_price = limit_price,
                order_type  = "limit"
            )

            if orderResponse.get("success") == False:
                print(f"Order replacement failed: {orderResponse.get('data', 'No reason')}")
                data = orderResponse.get("data", {})
                print(data.get("message", "No reason"))
                webhook_record.message = data.get("message", "No reason")
                await asyncio.sleep(settings.RETRY_BACKOFF_SECONDS)
                continue
            else:                
                order = orderResponse.get("data", {})

                print(order)
                status = order.get("status", "").lower()
                order_id = order.get("id")
                webhook_record.status = status
                webhook_record.order_id = order.get("id")
                webhook_record.limit_price = limit_price 

                print("Order ID For Attempts: {}", attempt,  order_id)    
            
        db.commit()
        db.refresh(webhook_record)
        
        print(f"Attempt {attempt + 1}: Order status: {status}")
        await asyncio.sleep(settings.RETRY_BACKOFF_SECONDS)

    db.commit()    
    return {
        "id": str(webhook_record.id),
        'message': webhook_record.message,
        "status": str(webhook_record.status),
    }

    

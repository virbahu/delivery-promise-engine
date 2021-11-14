import numpy as np
from datetime import datetime, timedelta
def promise_date(order, inventory, capacity, current_date="2022-06-01"):
    today=datetime.strptime(current_date,"%Y-%m-%d")
    items_available=all(inventory.get(item,0)>=qty for item,qty in order["items"].items())
    pick_days=1 if sum(order["items"].values())<10 else 2
    zone=order.get("zone","standard")
    ship_days={"express":1,"standard":3,"economy":5,"remote":7}.get(zone,3)
    if not items_available:
        backorder_days=max(inventory.get(item,0)-qty for item,qty in order["items"].items() if inventory.get(item,0)<qty)
        pick_days+=abs(backorder_days)+3
    daily_cap=capacity.get("daily_orders",500)
    queue=capacity.get("current_queue",0)
    queue_days=max(0,queue//daily_cap)
    total_days=pick_days+ship_days+queue_days
    promise=today+timedelta(days=total_days)
    if promise.weekday()>=5: promise+=timedelta(days=7-promise.weekday())
    confidence=0.95 if items_available else 0.75
    return {"promise_date":promise.strftime("%Y-%m-%d"),"business_days":total_days,
            "confidence":confidence,"available":items_available,"breakdown":{"pick":pick_days,"ship":ship_days,"queue":queue_days}}
if __name__=="__main__":
    order={"items":{"SKU-A":2,"SKU-B":1},"zone":"standard"}
    inv={"SKU-A":50,"SKU-B":5}; cap={"daily_orders":200,"current_queue":150}
    print(promise_date(order,inv,cap))

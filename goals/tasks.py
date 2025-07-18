from django.core.cache import cache
from django.db.models import DecimalField, ExpressionWrapper, F, Sum

from celery import shared_task
from goals.models import Contribution
from src.settings import logger


@shared_task
def store_supplier_sales_summary():
    supplier_totals = {}
    discounted_total_expr = F("quantity") * F("value") * (1 - F("discount"))

    # Efficient aggregation query
    totals = Contribution.objects.values("supplier_id").annotate(
        total_sales=Sum(ExpressionWrapper(discounted_total_expr, output_field=DecimalField()))
    )

    # Store in Redis
    for item in totals:
        supplier_id = item["supplier_id"]
        total = float(item["total_sales"] or 0)
        cache.set(f"supplier:{supplier_id}:total_sales", total)

    # (Optional) Also store the whole dict if needed
    cache.set("supplier_totals", supplier_totals)

    total_sales = cache.get("supplier:23:total_sales")

    logger.info(f"store_supplier_sales_summary {total_sales}")

    return supplier_totals

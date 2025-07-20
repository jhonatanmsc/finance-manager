from django.core.cache import cache
from django.db.models import DecimalField, ExpressionWrapper, F, Sum

from celery import shared_task
from goals.models import Contribution
from src.settings import logger


@shared_task
def store_supplier_totals_summary():
    supplier_totals = {}
    discounted_total_expr = F("quantity") * F("value") * (1 - F("discount"))

    # Efficient aggregation query
    totals = Contribution.objects.values("supplier_id").annotate(
        total_contributions=Sum(ExpressionWrapper(discounted_total_expr, output_field=DecimalField()))
    )

    # Store in Redis
    for item in totals:
        supplier_id = item["supplier_id"]
        total = float(item["total_contributions"] or 0)
        cache.set(f"supplier:{supplier_id}:total_contributions", total)

    # (Optional) Also store the whole dict if needed
    cache.set("supplier_totals", supplier_totals)

    logger.info("Supplier's contributions total stored")

    return supplier_totals


@shared_task
def store_goal_totals_summary():
    goal_totals = {}
    discounted_total_expr = F("quantity") * F("value") * (1 - F("discount"))

    # Efficient aggregation query
    totals = Contribution.objects.values("goal_id").annotate(
        total_contributions=Sum(ExpressionWrapper(discounted_total_expr, output_field=DecimalField()))
    )

    # Store in Redis
    for item in totals:
        supplier_id = item["goal_id"]
        total = float(item["total_contributions"] or 0)
        cache.set(f"goal:{supplier_id}:total_contributions", total)

    # (Optional) Also store the whole dict if needed
    cache.set("goal_totals", goal_totals)

    logger.info("Goal's contributions total stored")

    return goal_totals

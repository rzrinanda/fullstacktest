import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType
from datetime import datetime, timedelta
from django.db.models import Sum
from dateutil.relativedelta import relativedelta 


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = []

    pk = graphene.String()

class PresetRangeFields(graphene.ObjectType):
    category = graphene.String()
    amount = graphene.Float()

class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)

    def resolve_transactions(self, info):
        return Transaction.objects.all().order_by("-created_at")

    # EXTEND THIS CODE
    
class GetTransactionStatsQueries(graphene.ObjectType):
    transaction_stats = graphene.List(PresetRangeFields, presetRange=graphene.String())

    def resolve_transaction_stats(self, info, presetRange):

        if presetRange == "LAST_7_DAYS":
            today = datetime.now()
            date_before = str(today - timedelta(days=7))
            result = Transaction.objects.filter(created_at__gte=date_before).values('category').order_by('category').annotate(amount=Sum('amount'))
            return list(result)

        elif presetRange == "LAST_7_WEEKS":
            today = datetime.now()
            date_before = str(today - timedelta(weeks=7))
            result = Transaction.objects.filter(created_at__gte=date_before).values('category').order_by('category').annotate(amount=Sum('amount'))
            return list(result)

        elif presetRange == "LAST_7_MONTHS":
            today = datetime.now()
            date_before = str(today - relativedelta(months=7))
            result = Transaction.objects.filter(created_at__gte=date_before).values('category').order_by('category').annotate(amount=Sum('amount'))
            return list(result)


class GetTransactionSeriesQueries(graphene.ObjectType):
    transaction_series = graphene.List(PresetRangeFields, presetRange=graphene.String())

    def resolve_transaction_series(self, info, presetRange):

        if presetRange == "LAST_7_DAYS":
            today = datetime.now()
            date_before = str(today - timedelta(days=7))
            result = Transaction.objects.filter(created_at__gte=date_before).values('created_at').order_by('created_at').annotate(amount=Sum('amount'))
            resp = []
            for res in result:
                resp.append({
                    "key": res["created_at"],
                    "amount": res["amount"]
                    })
            return resp

        if presetRange == "LAST_7_WEEKS":
            today = datetime.now()
            resp = []

            start_date, end_date = "", ""
            for _ in range(1, 8):
                start_date = today - timedelta(weeks=1)
                end_date = today
                today = start_date
                result = Transaction.objects.filter(created_at__range=(start_date, end_date)).aggregate(sum=Sum('amount'))
                resp.append({
                    "key": start_date,
                    "amount": result["sum"]
                    })
            return resp

        if presetRange == "LAST_7_MONTHS":
            today = datetime.now()
            resp = []

            start_date, end_date = "", ""
            for _ in range(1, 8):
                start_date = today - relativedelta(months=1)
                end_date = today
                today = start_date
                result = Transaction.objects.filter(created_at__range=(start_date, end_date)).aggregate(sum=Sum('amount'))
                resp.append({
                    "key": start_date,
                    "amount": result["sum"]
                    })
            return resp

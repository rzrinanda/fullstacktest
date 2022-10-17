import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType
import datetime as DT



class TransactionNode(DjangoObjectType):
    today = DT.date.today()
    week_ago = today - DT.timedelta(days=7)
    PRESET_RANGE_TYPE = (
        ("LAST_7_DAYS", week_ago), 
        ("LAST_7_WEEKS", "LAST_7_WEEKS"), 
        ("LAST_7_MONTHS", "LAST_7_MONTHS")
        )
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = []

    pk = graphene.String()


class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)
    transaction_stats = graphene.Field(TransactionNode)

    def resolve_transactions(self, info):
        return Transaction.objects.all().order_by("-created_at")

    def resolve_transaction_stats(self, info, preset_range=None):
        try:
            #get preset range and useing django filter lt & gt
            return Transaction.objects.all().order_by("-created_at")
        except Transaction.DoesNotExist:
            return None
        
    # EXTEND THIS CODE

import logging
import unittest
from pathlib import Path

from dbtmetabase.dbt import (
    DbtReader,
    MetabaseColumn,
    MetabaseModel,
    ModelType,
    NullValue,
)


class TestDbtReader(unittest.TestCase):
    def setUp(self):
        """Must specify dbt root dir"""
        self.reader = DbtReader(
            manifest_path=str(
                Path("tests")
                / "fixtures"
                / "sample_project"
                / "target"
                / "manifest.json"
            ),
            database="test",
            schema="public",
        )
        logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    def test_read_models(self):
        models = self.reader.read_models()
        expectation = [
            MetabaseModel(
                name="orders",
                schema="PUBLIC",
                description="This table has basic information about orders, as well as some derived facts based on payments",
                model_type=ModelType.nodes,
                source=None,
                unique_id="model.jaffle_shop.orders",
                columns=[
                    MetabaseColumn(
                        name="ORDER_ID",
                        description="This is a unique identifier for an order",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="CUSTOMER_ID",
                        description="Foreign key to the customers table",
                        meta_fields={},
                        semantic_type="type/FK",
                        visibility_type=None,
                        fk_target_table="PUBLIC.CUSTOMERS",
                        fk_target_field="CUSTOMER_ID",
                    ),
                    MetabaseColumn(
                        name="ORDER_DATE",
                        description="Date (UTC) that the order was placed",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="STATUS",
                        description="Orders can be one of the following statuses:\n\n| status         | description                                                                                                            |\n|----------------|------------------------------------------------------------------------------------------------------------------------|\n| placed         | The order has been placed but has not yet left the warehouse                                                           |\n| shipped        | The order has ben shipped to the customer and is currently in transit                                                  |\n| completed      | The order has been received by the customer                                                                            |\n| return_pending | The customer has indicated that they would like to return the order, but it has not yet been received at the warehouse |\n| returned       | The order has been returned by the customer and received at the warehouse                                              |",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="AMOUNT",
                        description="Total amount (AUD) of the order",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="CREDIT_CARD_AMOUNT",
                        description="Amount of the order (AUD) paid for by credit card",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="COUPON_AMOUNT",
                        description="Amount of the order (AUD) paid for by coupon",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="BANK_TRANSFER_AMOUNT",
                        description="Amount of the order (AUD) paid for by bank transfer",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="GIFT_CARD_AMOUNT",
                        description="Amount of the order (AUD) paid for by gift card",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                ],
            ),
            MetabaseModel(
                name="customers",
                schema="PUBLIC",
                description="This table has basic information about a customer, as well as some derived facts based on a customer's orders",
                model_type=ModelType.nodes,
                source=None,
                unique_id="model.jaffle_shop.customers",
                columns=[
                    MetabaseColumn(
                        name="CUSTOMER_ID",
                        description="This is a unique identifier for a customer",
                        meta_fields={},
                        semantic_type=None,  # This is a PK field, should not be detected as FK
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="FIRST_NAME",
                        description="Customer's first name. PII.",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="LAST_NAME",
                        description="Customer's last name. PII.",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="FIRST_ORDER",
                        description="Date (UTC) of a customer's first order",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="MOST_RECENT_ORDER",
                        description="Date (UTC) of a customer's most recent order",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="NUMBER_OF_ORDERS",
                        description="Count of the number of orders a customer has placed",
                        meta_fields={},
                        semantic_type=NullValue,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="TOTAL_ORDER_AMOUNT",
                        description="Total value (AUD) of a customer's orders",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                ],
            ),
            MetabaseModel(
                name="stg_orders",
                schema="PUBLIC",
                description="",
                model_type=ModelType.nodes,
                source=None,
                unique_id="model.jaffle_shop.stg_orders",
                columns=[
                    MetabaseColumn(
                        name="ORDER_ID",
                        description="",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="STATUS",
                        description="",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                ],
            ),
            MetabaseModel(
                name="stg_payments",
                schema="PUBLIC",
                description="",
                model_type=ModelType.nodes,
                source=None,
                unique_id="model.jaffle_shop.stg_payments",
                columns=[
                    MetabaseColumn(
                        name="PAYMENT_ID",
                        description="",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                    MetabaseColumn(
                        name="PAYMENT_METHOD",
                        description="",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    ),
                ],
            ),
            MetabaseModel(
                name="stg_customers",
                schema="PUBLIC",
                description="",
                model_type=ModelType.nodes,
                source=None,
                unique_id="model.jaffle_shop.stg_customers",
                columns=[
                    MetabaseColumn(
                        name="CUSTOMER_ID",
                        description="",
                        meta_fields={},
                        semantic_type=None,
                        visibility_type=None,
                        fk_target_table=None,
                        fk_target_field=None,
                    )
                ],
            ),
        ]
        self.assertEqual(models, expectation)
        logging.info("Done")

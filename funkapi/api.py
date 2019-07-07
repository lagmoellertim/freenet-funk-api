import boto3
import requests
import datetime
from warrant.aws_srp import AWSSRP

from funkapi.graphql_schema import schema

class FunkAPI:
    """
    Freenet FUNK API helper library
    """

    API_ENDPOINT = "https://appapi.funk.services/"
    API_KEY = "FZ3OkFFfdMahh4a1xagOnaon39pUpml732kkb2Aw"
    AWS_REGION = "eu-central-1"
    AWS_POOL_ID = "eu-central-1_ZPDpzBJy4"
    AWS_CLIENT_ID = "3asd34f9vfrg6pd2mrbqhn3g3r"

    def __init__(self, username, password, token=None, always_test_token=False,
                 ignore_token_check=False, ignore_token_retry=True, autoload_data=True):
        """
        Initialise API.

        :param username: Account E-Mail
        :param password: Account Password
        :param token: AWS Cognito JWT token
        :param always_test_token: Whether the validity of a token should be tested after each request
        :param ignore_token_check: Whether a token should be checked at all (when supplied via the token param)
        :param ignore_token_retry: Whether to stop using the user/pass params if the supplied token is wrong
        :param autoload_data: Whether to automatically load the data on initialization
        """

        self.username = username
        self.password = password
        self.always_test_token = always_test_token
        self.ignore_token_check = ignore_token_check
        self.ignore_token_retry = ignore_token_retry

        self.client = boto3.client('cognito-idp', region_name=self.AWS_REGION,
                                   aws_access_key_id="", aws_secret_access_key="")

        self.aws = AWSSRP(username=self.username, password=self.password,
                          pool_id=self.AWS_POOL_ID,
                          client_id=self.AWS_CLIENT_ID, client=self.client)

        self.token = None
        self.getToken(token=token)

        self.data = None
        if autoload_data:
            self.getData()

    def apiRequest(self, json, token=None):
        """
        Trigger API endpoint and request data.

        :param json: graphQL request schema
        :param token: AWS cognito JWT token
        :return: API response
        """

        token = token if token is not None else self.getToken()

        req = requests.post(self.API_ENDPOINT, json=json,
                            headers={
                                "x-api-key": self.API_KEY,
                                "Authorization": "Bearer " + token,
                                "apollographql-client-version": "1.0.1 (1143)",
                                "apollographql-client-name": "freenet FUNK iOS"
                            })
        return req.json()

    def getToken(self, refresh=False, token=None):
        """
        Returns a valid aws cognito JWT token.

        :param refresh: Disallow caching
        :param token: AWS cognito JWT token
        :return: AWS cognito JWT token
        """

        if token is not None:
            if self.testToken(token) or self.ignore_token_retry:
                self.token = token
                return self.token

            self.getToken(refresh=True)

        if self.token is None or refresh or (
                False if not self.always_test_token else not self.testToken(self.token)):
            self.token = self.aws.authenticate_user()["AuthenticationResult"]["AccessToken"]

        return self.token

    def testToken(self, token):
        """
        Test validity of authorization token.

        :param token: AWS cognito JWT token
        :return: Boolean whether the token is valid (True) or not (False)
        """

        if token is None:
            return False

        if not self.ignore_token_check:
            json = {"operationName": "CustomerForDashboardQuery", "variables": {},
                    "query": "query CustomerForDashboardQuery { me { id } }"}

            result = self.apiRequest(json, token=token)

            if "errors" in result.keys():
                return False

        return True

    def getData(self, refresh=False):
        """
        Get data from endpoint.

        :param refresh: Ignore cache / Force Refresh
        :return: Data
        """

        json = {"operationName": "CustomerForDashboardQuery", "variables": {},
                "query": schema["get_data"]}
        if self.data is None or refresh:
            self.data = self.apiRequest(json)

        return self.data

    def getPersonalInfo(self, refresh_data=False):
        """
        Get personal data.

        :param refresh_data: Ignore cache / Force Refresh
        :return: Personal data
        """

        data = self.getData(refresh=refresh_data)["data"]["me"]
        personal_info = {"id": data["id"], **data["details"]}
        del personal_info["__typename"]

        return personal_info

    def getOrderedProducts(self, refresh_data=False):
        """
        Get ordered products (e.g. sim cards).

        :param refresh_data: Ignore cache / Force Refresh
        :return: A list of all ordered Products
        """

        return self.getData(refresh=refresh_data)["data"]["me"]["customerProducts"]

    def getCurrentPlan(self, refresh_data=False):
        """
        Get current plan.

        :param refresh_data: Ignore cache / Force Refresh
        :return: Current plan
        """

        now = datetime.datetime.now(datetime.timezone.utc)
        currentPlan = None
        for plan in self.getData(refresh=refresh_data)["data"]["me"]["customerProducts"][0]["tariffs"]:
            planStart = datetime.datetime.strptime(plan["starts"], "%Y-%m-%dT%H:%M:%S.%f%z")
            if planStart > now:
                continue
            currentPlan = plan
            
        return currentPlan

    def orderPlan(self, plan_id, product_id=None, refresh_data=True):
        """
        Order a plan.

        :param plan_id: Id of plan which should be ordered
        :param product_id: The sim card id the plan should be applied to
        :param refresh_data: Ignore cache / Force Refresh
        :return: Result of order
        """

        if product_id is None:
            product_id = self.getOrderedProducts()[0]["id"]

        json = {"operationName": "AddTariffToProductMutation",
                "variables": {"productID": product_id, "tariffID": str(plan_id)},
                "query": schema["order_plan"]}
        result = self.apiRequest(json)

        self.getData(refresh=refresh_data)

        return result

    def removeProduct(self, personal_plan_id, refresh_data=True):
        """
        Remove/Deactivate an active plan.

        :param personal_plan_id: Id of current plan
        :param refresh_data: Ignore cache / Force Refresh
        :return: Result of removal
        """

        json = {"operationName": "TerminateTariffMutation",
                "variables": {"tariffID": personal_plan_id},
                "query": schema["remove_product"]}

        result = self.apiRequest(json)

        self.getData(refresh=refresh_data)

        return result

    def order1GBPlan(self, **kwargs):
        """
        Order 1GB plan.

        :param kwargs: More details at FunkAPI.orderPlan
        :return: Result of order
        """

        return self.orderPlan(9, **kwargs)

    def orderUnlimitedPlan(self, **kwargs):
        """
        Order unlimited plan.

        :param kwargs: More details at FunkAPI.orderPlan
        :return: Result of order
        """

        return self.orderPlan(8, **kwargs)

    def startPause(self, **kwargs):
        """
        Start pause mode.

        :param kwargs: More details at FunkAPI.orderPlan
        :return: Result of order
        """

        return self.orderPlan(42, **kwargs)

    def stopLatestPlan(self, product_index=0, **kwargs):
        """
        Stop current plan.

        :param product_index: The sim card id of which the plan should be stopped
        :param kwargs: More details at FunkAPI.removeProduct
        :return: Result of order
        """

        personal_plan_id = self.getOrderedProducts()[product_index]["tariffs"][-1]["id"]
        return self.removeProduct(personal_plan_id, **kwargs)
